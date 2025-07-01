"""
Phase 2: Product Price Scraping Implementation

This file shows exactly how automated price monitoring will work in Phase 2.
It demonstrates real scraping of UK retailers with actual price extraction.
"""

import requests
from bs4 import BeautifulSoup
import re
from decimal import Decimal
from urllib.parse import urlparse
import time
import random

class UKPriceScraper:
    """
    UK-focused price scraper for major retailers
    Converts all prices to GBP and handles UK-specific formatting
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
    
    def get_random_headers(self):
        """Generate random headers to avoid detection"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def extract_price_gbp(self, price_text):
        """
        Extract GBP price from various text formats
        Examples: "£19.99", "£1,234.56", "19.99", "From £15.00"
        """
        if not price_text:
            return None
            
        # Remove common prefixes and clean text
        price_text = price_text.replace('From ', '').replace('from ', '')
        price_text = price_text.replace('£', '').replace(',', '')
        
        # Extract decimal number
        price_match = re.search(r'\d+\.?\d*', price_text)
        if price_match:
            try:
                return Decimal(price_match.group())
            except:
                return None
        return None
    
    def scrape_amazon_uk(self, product_url):
        """
        Scrape price from Amazon UK
        Real example: https://www.amazon.co.uk/dp/B08N5WRWNW
        """
        headers = self.get_random_headers()
        
        try:
            response = self.session.get(product_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Amazon UK price selectors (ordered by reliability)
            price_selectors = [
                'span.a-price.a-text-price.a-size-medium.apexPriceToPay span.a-offscreen',
                'span.a-price-whole',
                '.a-price .a-offscreen',
                '#price_inside_buybox',
                '.a-price-current .a-offscreen',
                '.a-text-price .a-offscreen'
            ]
            
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text().strip()
                    price = self.extract_price_gbp(price_text)
                    if price:
                        return {
                            'price': price,
                            'currency': 'GBP',
                            'source': 'Amazon UK',
                            'selector_used': selector,
                            'raw_text': price_text
                        }
            
            return None
            
        except Exception as e:
            print(f"Amazon UK scraping error: {e}")
            return None
    
    def scrape_argos(self, product_url):
        """
        Scrape price from Argos
        Real example: https://www.argos.co.uk/product/1234567
        """
        headers = self.get_random_headers()
        
        try:
            response = self.session.get(product_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Argos price selectors
            price_selectors = [
                '[data-test="product-price"] .sr-only',
                '.prices-current',
                '.price-current',
                '[data-testid="price"]'
            ]
            
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text().strip()
                    price = self.extract_price_gbp(price_text)
                    if price:
                        return {
                            'price': price,
                            'currency': 'GBP',
                            'source': 'Argos',
                            'selector_used': selector,
                            'raw_text': price_text
                        }
            
            return None
            
        except Exception as e:
            print(f"Argos scraping error: {e}")
            return None
    
    def scrape_ebay_uk(self, product_url):
        """
        Scrape price from eBay UK
        Real example: https://www.ebay.co.uk/itm/123456789
        """
        headers = self.get_random_headers()
        
        try:
            response = self.session.get(product_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # eBay UK price selectors
            price_selectors = [
                '.notranslate[itemprop="price"]',
                '.u-flL.condText .notranslate',
                '.vi-price .notranslate',
                '#prcIsum .notranslate',
                '.mm-saleDscPrc .notranslate'
            ]
            
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text().strip()
                    price = self.extract_price_gbp(price_text)
                    if price:
                        return {
                            'price': price,
                            'currency': 'GBP',
                            'source': 'eBay UK',
                            'selector_used': selector,
                            'raw_text': price_text
                        }
            
            return None
            
        except Exception as e:
            print(f"eBay UK scraping error: {e}")
            return None
    
    def detect_site_and_scrape(self, product_url):
        """
        Auto-detect retailer and scrape price
        This is the main function that will be called by Celery tasks
        """
        domain = urlparse(product_url).netloc.lower()
        
        # Add random delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        
        if 'amazon.co.uk' in domain:
            return self.scrape_amazon_uk(product_url)
        elif 'argos.co.uk' in domain:
            return self.scrape_argos(product_url)
        elif 'ebay.co.uk' in domain:
            return self.scrape_ebay_uk(product_url)
        else:
            # Generic scraper for unknown sites
            return self.generic_price_scrape(product_url)
    
    def generic_price_scrape(self, product_url):
        """
        Generic price scraper for unknown sites
        Looks for common price patterns
        """
        headers = self.get_random_headers()
        
        try:
            response = self.session.get(product_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Common price selectors across e-commerce sites
            generic_selectors = [
                '[class*="price"]',
                '[id*="price"]',
                '[class*="cost"]',
                '[class*="amount"]',
                '.money',
                '.currency'
            ]
            
            for selector in generic_selectors:
                price_elems = soup.select(selector)
                for elem in price_elems:
                    price_text = elem.get_text().strip()
                    if '£' in price_text or re.search(r'\d+\.\d{2}', price_text):
                        price = self.extract_price_gbp(price_text)
                        if price and price > 0:
                            return {
                                'price': price,
                                'currency': 'GBP',
                                'source': 'Generic Scraper',
                                'selector_used': selector,
                                'raw_text': price_text
                            }
            
            return None
            
        except Exception as e:
            print(f"Generic scraping error: {e}")
            return None


# Phase 2: Celery Task Integration

from celery import shared_task
from django.utils import timezone
from products.models import Product, PriceHistory, TrackedProduct, DealAlert

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def scrape_and_update_price(self, tracked_product_id):
    """
    Main Celery task for automated price monitoring
    This runs in the background every few hours
    """
    try:
        tracked_product = TrackedProduct.objects.get(id=tracked_product_id)
        product = tracked_product.product
        
        # Initialize scraper
        scraper = UKPriceScraper()
        
        # Scrape current price
        price_data = scraper.detect_site_and_scrape(product.url)
        
        if price_data and price_data['price']:
            old_price = product.current_price
            new_price = price_data['price']
            
            # Update product with new price
            product.current_price = new_price
            product.last_checked = timezone.now()
            product.save()
            
            # Create price history record
            PriceHistory.objects.create(
                product=product,
                price=new_price,
                timestamp=timezone.now(),
                source=price_data['source']
            )
            
            # Check if price dropped below user's target
            if new_price <= tracked_product.desired_price:
                # Create deal alert
                DealAlert.objects.create(
                    user=tracked_product.user,
                    product=product,
                    alert_price=new_price,
                    target_price=tracked_product.desired_price,
                    price_drop_amount=old_price - new_price if old_price else 0,
                    is_sent=False  # Will be processed by notification task
                )
                
                # Trigger notification task
                send_price_alert.delay(tracked_product.user.id, product.id, new_price)
            
            return f"Price updated: £{old_price} → £{new_price}"
        
        else:
            # Scraping failed - log and retry
            return f"Scraping failed for {product.url}"
            
    except Exception as e:
        # Exponential backoff retry
        raise self.retry(countdown=60 * (2 ** self.request.retries))


@shared_task
def scrape_all_products():
    """
    Scheduled task to scrape all tracked products
    Runs every 2-4 hours depending on subscription tier
    """
    # Get all active tracked products
    tracked_products = TrackedProduct.objects.filter(is_active=True)
    
    for tracked_product in tracked_products:
        # Free users: check every 24 hours
        # Premium users: check every 2-4 hours
        if tracked_product.user.profile.is_premium:
            delay = random.uniform(0, 3600)  # Random delay up to 1 hour
        else:
            delay = random.uniform(0, 7200)  # Random delay up to 2 hours
        
        # Schedule individual scraping task
        scrape_and_update_price.apply_async(
            args=[tracked_product.id],
            countdown=delay
        )
    
    return f"Scheduled scraping for {tracked_products.count()} products"


@shared_task
def send_price_alert(user_id, product_id, new_price):
    """
    Send price drop notification to user
    Will be implemented in Phase 3 with email/SMS
    """
    # Phase 3: Email notification implementation
    # Phase 3: SMS notification for premium users
    # Phase 3: WhatsApp notification integration
    pass


# Example Usage and Testing

if __name__ == "__main__":
    # Test the scraper with real URLs
    scraper = UKPriceScraper()
    
    # Test URLs (these would be real products)
    test_urls = [
        "https://www.amazon.co.uk/dp/B08N5WRWNW",  # Example product
        "https://www.argos.co.uk/product/1234567",    # Example product
        "https://www.ebay.co.uk/itm/123456789"       # Example product
    ]
    
    for url in test_urls:
        print(f"\nTesting: {url}")
        result = scraper.detect_site_and_scrape(url)
        if result:
            print(f"Price: £{result['price']}")
            print(f"Source: {result['source']}")
        else:
            print("Scraping failed")
