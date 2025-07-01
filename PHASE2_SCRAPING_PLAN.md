# Phase 2: Web Scraping Implementation Plan

## Site-Specific Scraping Strategies

### Amazon UK (amazon.co.uk)
- **Method**: BeautifulSoup + rotating User-Agents
- **Price Selectors**: `.a-price-whole`, `.a-offscreen`, `#price_inside_buybox`
- **Challenges**: Anti-bot measures, CAPTCHA
- **Solutions**: Request throttling, proxy rotation, session management

### eBay UK (ebay.co.uk)
- **Method**: BeautifulSoup (simpler structure)
- **Price Selectors**: `.notranslate`, `.u-flL.condText`, `.vi-price .notranslate`
- **Auction Logic**: Handle both auction and Buy-It-Now prices
- **Currency**: Already in GBP

### Argos (argos.co.uk)
- **Method**: BeautifulSoup
- **Price Selectors**: `.prices-current`, `.price-current`, `[data-test="product-price"]`
- **Stock Status**: Check availability alongside price

### Currys PC World (currys.co.uk)
- **Method**: Selenium (heavy JavaScript)
- **Price Selectors**: `[data-testid="price"]`, `.price`, `.current-price`
- **Dynamic Loading**: Wait for JavaScript price updates

## Implementation Architecture

### 1. Scraper Factory Pattern
```python
class ScraperFactory:
    scrapers = {
        'amazon.co.uk': AmazonUKScraper,
        'ebay.co.uk': EbayUKScraper,
        'argos.co.uk': ArgosScraper,
        'currys.co.uk': CurrysScraper
    }
    
    @classmethod
    def get_scraper(cls, url):
        domain = extract_domain(url)
        return cls.scrapers.get(domain, GenericScraper)()
```

### 2. Celery Task Implementation
```python
from celery import shared_task
from .models import Product, PriceHistory

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def scrape_product_price(self, product_id):
    """
    Scrape current price for a specific product
    """
    try:
        product = Product.objects.get(id=product_id)
        scraper = ScraperFactory.get_scraper(product.url)
        
        current_price = scraper.get_price(product.url)
        
        if current_price:
            # Update product
            product.current_price = current_price
            product.last_checked = timezone.now()
            product.save()
            
            # Create price history record
            PriceHistory.objects.create(
                product=product,
                price=current_price,
                timestamp=timezone.now()
            )
            
            # Check for price alerts
            check_price_alerts.delay(product_id, current_price)
            
        return f"Price updated: £{current_price}"
        
    except Exception as e:
        # Retry logic with exponential backoff
        raise self.retry(countdown=60 * (2 ** self.request.retries))
```

### 3. Scheduled Price Monitoring
```python
# In celery.py beat_schedule
beat_schedule = {
    'scrape-all-products': {
        'task': 'products.tasks.scrape_all_products',
        'schedule': crontab(minute=0, hour='*/2'),  # Every 2 hours
    },
    'priority-product-check': {
        'task': 'products.tasks.scrape_priority_products', 
        'schedule': crontab(minute='*/30'),  # Every 30 minutes for premium users
    },
}
```

## Data Quality & Reliability

### 1. Price Validation
- **Format Standardization**: Convert all prices to GBP decimal format
- **Outlier Detection**: Flag suspicious price changes (>50% change)
- **Historical Comparison**: Validate against recent price history
- **Manual Verification**: Admin interface for price correction

### 2. Error Handling
- **Retry Logic**: 3 attempts with exponential backoff
- **Fallback Sources**: Try alternative selectors/methods
- **Monitoring**: Log failed scrapes for analysis
- **User Notification**: Inform users of tracking issues

### 3. Anti-Bot Countermeasures
- **User-Agent Rotation**: Random browser identities
- **Request Throttling**: Respect robots.txt and rate limits
- **Proxy Rotation**: Distribute requests across IP addresses
- **Session Management**: Maintain cookies and sessions
- **CAPTCHA Handling**: Manual intervention workflows

## Compliance & Ethics

### 1. Legal Compliance
- **Terms of Service**: Review and comply with site ToS
- **Robots.txt**: Respect crawling guidelines
- **Rate Limiting**: Reasonable request frequency
- **Data Usage**: Price monitoring only, no resale

### 2. Technical Best Practices
- **Caching**: Avoid duplicate requests
- **Efficient Selectors**: Minimize page load requirements
- **Resource Management**: Clean up browser instances
- **Error Logging**: Track and analyze failures

## Scalability Considerations

### 1. Infrastructure
- **Redis Queue**: Handle thousands of scraping tasks
- **Database Optimization**: Efficient price history storage
- **CDN Integration**: Cache product images and metadata
- **Monitoring**: Track scraping performance and success rates

### 2. Business Logic
- **Subscription Tiers**: 
  - Free: Check every 24 hours
  - Premium: Check every 2-4 hours
- **Priority Products**: More frequent checks for active deals
- **Bulk Operations**: Efficient batch processing

This comprehensive approach ensures reliable, scalable, and compliant price monitoring across major UK retailers.
