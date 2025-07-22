"""
Phase 2: Product Scraping Tasks

This module implements the core web scraping functionality for automated price monitoring.
It includes site-specific scrapers, generic fallbacks, and Celery task integration.

Key Features:
- Multi-site scraper support (Amazon UK, Argos, eBay UK, etc.)
- Robust error handling and retry logic
- Price validation and format standardization
- Background task processing with Celery
- Rate limiting and anti-bot measures
"""

import requests
from bs4 import BeautifulSoup
import re
from decimal import Decimal, InvalidOperation
from urllib.parse import urlparse
import time
import random
from celery import shared_task
from django.utils import timezone
from django.conf import settings
import logging

from .models import Product, PriceHistory, TrackedProduct, PriceAlert
from users.models import UserProfile

# Set up logging
logger = logging.getLogger(__name__)


class PriceScraper:
    """
    Main price scraping class with support for multiple UK retailers.
    Handles site-specific scraping and generic fallback.
    """

    def __init__(self):
        self.session = requests.Session()
        self.user_agents = [
            # Updated, realistic user-agents for better reliability
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        ]
        self.session.headers.update(self._get_random_headers())

    def _get_random_headers(self):
        """Generate random headers to avoid detection"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def _extract_price_gbp(self, price_text):
        """
        Extract GBP price from various text formats
        Examples: "£19.99", "£1,234.56", "19.99", "From £15.00"
        """
        if not price_text:
            return None
            
        # Clean the text
        price_text = str(price_text).strip()
        price_text = re.sub(r'[^\d.,£]', '', price_text)
        price_text = price_text.replace('£', '').replace(',', '')
        
        # Extract decimal number
        price_match = re.search(r'\d+\.?\d*', price_text)
        if price_match:
            try:
                price_value = Decimal(price_match.group())
                # Validate reasonable price range (£0.01 to £50,000)
                if 0.01 <= price_value <= 50000:
                    return price_value
            except (InvalidOperation, ValueError):
                pass
        return None
    
    def _safe_request(self, url, timeout=10):
        """Make a safe HTTP request with error handling and anti-bot detection"""
        try:
            # Add random delay to avoid rate limiting
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()

            # Check for anti-bot or CAPTCHA pages (Amazon/eBay)
            page_text = response.text.lower()
            if ("captcha" in page_text or "robot check" in page_text or "enter the characters you see below" in page_text):
                logger.warning(f"Anti-bot page detected for {url}")
                return None

            return response
        except requests.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None

    def scrape_amazon_uk(self, product_url):
        """Scrape price from Amazon UK"""
        response = self._safe_request(product_url)
        if not response:
            logger.error(f"Failed to fetch Amazon UK page: {product_url}")
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Amazon UK price selectors (ordered by reliability)
        selectors = [
            'span.a-price.a-text-price.a-size-medium.apexPriceToPay span.a-offscreen',
            'span.a-price .a-offscreen',
            'span.a-price-whole',
            '#priceblock_ourprice',
            '#priceblock_dealprice',
            '#price_inside_buybox',
            '.a-price .a-offscreen',
            '.a-text-price .a-offscreen'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price = self._extract_price_gbp(element.get_text())
                if price:
                    return {
                        'price': price,
                        'source': 'Amazon UK',
                        'selector': selector,
                        'success': True
                    }
        
        return {'success': False, 'error': 'No price found'}
    
    def scrape_argos(self, product_url):
        """Scrape price from Argos"""
        response = self._safe_request(product_url)
        if not response:
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        selectors = [
            '[data-test="product-price"]',
            '.prices-current',
            '.price-current',
            '[data-testid="price"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price = self._extract_price_gbp(element.get_text())
                if price:
                    return {
                        'price': price,
                        'source': 'Argos',
                        'selector': selector,
                        'success': True
                    }
        
        return {'success': False, 'error': 'No price found'}
    
    def scrape_ebay_uk(self, product_url):
        """Scrape price from eBay UK"""
        response = self._safe_request(product_url)
        if not response:
            logger.error(f"Failed to fetch eBay UK page: {product_url}")
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        selectors = [
            '.notranslate[itemprop="price"]',
            '#prcIsum',
            '#mm-saleDscPrc',
            '.display-price',
            '.u-flL.condText .notranslate',
            '.vi-price .notranslate',
            '#prcIsum .notranslate'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price = self._extract_price_gbp(element.get_text())
                if price:
                    return {
                        'price': price,
                        'source': 'eBay UK',
                        'selector': selector,
                        'success': True
                    }
        
        return {'success': False, 'error': 'No price found'}
    
    def generic_scrape(self, product_url):
        """Generic scraper for unknown sites"""
        response = self._safe_request(product_url)
        if not response:
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Common price selectors
        selectors = [
            '[class*="price"]',
            '[id*="price"]',
            '[class*="cost"]',
            '.money',
            '.currency'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text().strip()
                if '£' in text:
                    price = self._extract_price_gbp(text)
                    if price:
                        return {
                            'price': price,
                            'source': 'Generic Scraper',
                            'selector': selector,
                            'success': True
                        }
        
        return {'success': False, 'error': 'No price found'}
    
    def scrape_price(self, product_url):
        """
        Main scraping method - auto-detects site and scrapes price
        """
        domain = urlparse(product_url).netloc.lower()
        
        try:
            if 'amazon.co.uk' in domain:
                return self.scrape_amazon_uk(product_url)
            elif 'argos.co.uk' in domain:
                return self.scrape_argos(product_url)
            elif 'ebay.co.uk' in domain:
                return self.scrape_ebay_uk(product_url)
            else:
                return self.generic_scrape(product_url)
        except Exception as e:
            logger.error(f"Scraping failed for {product_url}: {e}")
            return {'success': False, 'error': str(e)}


# Celery Tasks for Background Processing

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def scrape_product_price(self, tracked_product_id):
    """
    Celery task: Scrape price for a single tracked product and trigger alerts if needed.
    """
    try:
        tracked_product = TrackedProduct.objects.get(id=tracked_product_id)
        product = tracked_product.product
        
        logger.info(f"Scraping price for product: {product.name} ({product.url})")
        
        # Initialize scraper
        scraper = PriceScraper()
        
        # Scrape current price
        result = scraper.scrape_price(product.url)
        
        if result and result.get('success'):
            old_price = product.current_price
            new_price = result['price']
            
            # Update product with new price
            product.current_price = new_price
            product.last_checked = timezone.now()
            product.save()
            
            # Create price history record
            PriceHistory.objects.create(
                product=product,
                price=new_price,
                timestamp=timezone.now(),
                source=result.get('source', 'Unknown')
            )       
            
            
            # Check for price drop alerts using PriceAlert logic
            alerts = PriceAlert.objects.filter(tracked_product=tracked_product, is_enabled=True, is_triggered=False)
            for alert in alerts:
                if alert.check_price_drop():
                    alert.trigger_alert(product.current_price)
            
            return f"Success: £{old_price} → £{new_price} ({result['source']})"
        
        else:
            error_msg = result.get('error', 'Unknown error') if result else 'No response'
            logger.warning(f"Scraping failed for {product.url}: {error_msg}")
            return f"Failed: {error_msg}"
            
    except TrackedProduct.DoesNotExist:
        logger.error(f"TrackedProduct {tracked_product_id} not found")
        return f"Error: TrackedProduct {tracked_product_id} not found"
    
    except Exception as e:
        logger.error(f"Unexpected error in scrape_product_price: {e}")
        # Retry with exponential backoff
        raise self.retry(countdown=60 * (2 ** self.request.retries))


@shared_task
def scrape_all_products():
    """
    Celery task: Schedule scraping for all active tracked products.
    Premium users get more frequent checks.
    """
    # Get all active tracked products
    tracked_products = TrackedProduct.objects.filter(is_active=True).select_related('user__profile', 'product')
    
    premium_count = 0
    free_count = 0
    
    for tracked_product in tracked_products:
        try:
            profile = tracked_product.user.profile
            is_premium = profile.is_premium if profile else False
            
            # Calculate delay based on subscription tier
            if is_premium:
                # Premium: check every 2-4 hours with random delay
                delay = random.uniform(0, 3600)  # 0-1 hour delay
                premium_count += 1
            else:
                # Free: check every 24 hours with random delay
                delay = random.uniform(0, 7200)  # 0-2 hour delay
                free_count += 1
            
            # Schedule individual scraping task
            scrape_product_price.apply_async(
                args=[tracked_product.id],
                countdown=delay
            )
            
        except Exception as e:
            logger.error(f"Error scheduling scrape for tracked_product {tracked_product.id}: {e}")
    
    logger.info(f"Scheduled scraping: {premium_count} premium, {free_count} free products")
    return f"Scheduled: {premium_count} premium + {free_count} free = {tracked_products.count()} total"


@shared_task
def cleanup_old_price_history():
    """
    Celery task: Delete price history records older than 90 days.
    """
    from datetime import timedelta
    
    cutoff_date = timezone.now() - timedelta(days=90)
    
    # Delete price history older than 90 days
    deleted_count = PriceHistory.objects.filter(timestamp__lt=cutoff_date).delete()[0]
    
    logger.info(f"Cleaned up {deleted_count} old price history records")
    return f"Deleted {deleted_count} old price history records"


@shared_task
def update_product_metadata(product_id):
    """
    Celery task: Update product metadata (name, image, etc.) from the product page.
    """
    try:
        product = Product.objects.get(id=product_id)
        scraper = PriceScraper()
        
        response = scraper._safe_request(product.url)
        if not response:
            return f"Failed to fetch {product.url}"
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract product title
        title_selectors = ['title', 'h1', '.product-title', '[data-testid="product-title"]']
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text().strip()
                if title and len(title) > 10:  # Basic validation
                    product.name = title[:200]  # Limit length
                    break
        
        # Extract product image
        img_selectors = ['meta[property="og:image"]', '.product-image img', '.main-image img']
        for selector in img_selectors:
            element = soup.select_one(selector)
            if element:
                img_url = element.get('content') or element.get('src')
                if img_url:
                    product.image_url = img_url
                    break
        
        product.save()
        return f"Updated metadata for {product.name}"
        
    except Product.DoesNotExist:
        return f"Product {product_id} not found"
    except Exception as e:
        logger.error(f"Error updating product metadata: {e}")
        return f"Error: {e}"
