from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.utils import timezone
from decimal import Decimal

# Create your models here.

class Product(models.Model):
    """
    Model for products being tracked across e-commerce sites
    
    This is the central model that stores product information scraped
    from various e-commerce platforms. Multiple users can track the
    same product without data duplication.
    
    Design Logic:
    - Stores current price (updated by scraping tasks)
    - Maintains product metadata for identification
    - Tracks scraping statistics for performance monitoring
    """
    
    # Core product information
    name = models.CharField(max_length=255)                    # Product title from e-commerce site
    url = models.URLField(max_length=500, validators=[URLValidator()])  # Direct link to product page
    image_url = models.URLField(max_length=500, blank=True, null=True)  # Product image for UI
    current_price = models.DecimalField(max_digits=10, decimal_places=2)  # Latest scraped price
    
    # E-commerce site information for scraping optimization
    site_name = models.CharField(max_length=100, blank=True)   # Amazon, eBay, etc.
    product_id = models.CharField(max_length=100, blank=True)  # Site-specific product ID (ASIN, etc.)
    
    # Product classification for user browsing
    category = models.CharField(max_length=100, blank=True)    # Electronics, Clothing, etc.
    brand = models.CharField(max_length=100, blank=True)       # Brand name
    description = models.TextField(blank=True)                 # Product description
    
    # Tracking metadata for system monitoring
    is_active = models.BooleanField(default=True)              # Enable/disable scraping
    last_checked = models.DateTimeField(auto_now_add=True)     # Last scraping attempt (success or fail)
    last_scraped = models.DateTimeField(null=True, blank=True) # Last successful scrape
    scrape_count = models.IntegerField(default=0)              # Total scrapes performed
    scrape_failures = models.IntegerField(default=0)           # Failed scrape attempts
    
    # Audit trail
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=['site_name']),
            models.Index(fields=['category']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - £{self.current_price}"
    
    @property
    def domain(self):
        """Extract domain from product URL"""
        from urllib.parse import urlparse
        return urlparse(self.url).netloc
    
    @property
    def price_change_24h(self):
        """Get price change in last 24 hours"""
        from datetime import timedelta
        yesterday = timezone.now() - timedelta(days=1)
        
        recent_price = self.pricehistory_set.filter(
            timestamp__gte=yesterday
        ).order_by('timestamp').first()
        
        if recent_price:
            return self.current_price - recent_price.price
        return Decimal('0.00')
    
    @property
    def scrape_success_rate(self):
        """Calculate scraping success rate"""
        total_attempts = self.scrape_count + self.scrape_failures
        if total_attempts == 0:
            return 100.0
        return (self.scrape_count / total_attempts) * 100
    
    @property
    def price_history(self):
        """Get price history for this product"""
        return self.pricehistory_set.all().order_by('-timestamp')
    
    @property
    def lowest_price(self):
        """Get the lowest recorded price"""
        lowest = self.pricehistory_set.aggregate(min_price=models.Min('price'))
        return lowest['min_price'] or self.current_price


class PriceHistory(models.Model):
    """
    Model to track price changes over time
    
    This model creates a historical record of price changes for analysis
    and trend detection. It enables:
    - Price drop percentage calculations
    - Historical price charts for users
    - Deal validation (ensuring price drops are legitimate)
    
    Design Logic:
    - One record per price scrape per product
    - Immutable records for audit trail
    - Indexed by product and timestamp for fast queries
    """
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to tracked product
    price = models.DecimalField(max_digits=10, decimal_places=2)    # Price at this point in time
    timestamp = models.DateTimeField(auto_now_add=True)             # When price was recorded
    
    # Additional tracking data for scraping reliability
    was_available = models.BooleanField(default=True)               # Product availability status
    source = models.CharField(max_length=50, default='manual')      # Which scraper collected this (Amazon UK, Argos, etc.)
    
    class Meta:
        db_table = 'price_history'
        verbose_name = 'Price History'
        verbose_name_plural = 'Price Histories'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['product', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.product.name} - ${self.price} at {self.timestamp}"


class TrackedProduct(models.Model):
    """
    Model for products that users are tracking
    
    This is the many-to-many relationship between Users and Products
    with additional user-specific tracking preferences.
    
    Business Logic:
    - Each user can set their own desired price for the same product
    - Customizable notification thresholds per user
    - Tracks notification history to prevent spam
    
    Design Logic:
    - Unique constraint prevents duplicate tracking
    - Supports different alert preferences per user
    - Enables subscription tier limits (free users: 3 products)
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)        # Who is tracking this product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # What product is being tracked
    desired_price = models.DecimalField(max_digits=10, decimal_places=2)  # User's target price
    
    # Notification preferences - user-specific settings
    notify_on_price_drop = models.BooleanField(default=True)        # Alert on any price decrease
    notify_on_availability = models.BooleanField(default=True)      # Alert when back in stock
    minimum_discount_percent = models.DecimalField(                 # Minimum % drop to trigger alert
        max_digits=5, 
        decimal_places=2, 
        default=Decimal('10.00')
    )
    
    # Tracking status and spam prevention
    is_active = models.BooleanField(default=True)                   # User can pause tracking
    last_notification_sent = models.DateTimeField(blank=True, null=True)  # Prevent notification spam
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tracked_products'
        verbose_name = 'Tracked Product'
        verbose_name_plural = 'Tracked Products'
        unique_together = ['user', 'product']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.user.username} tracking {self.product.name}"
    
    @property
    def current_discount_percent(self):
        """Calculate current discount percentage from desired price"""
        if self.desired_price and self.product.current_price:
            discount = ((self.desired_price - self.product.current_price) / self.desired_price) * 100
            return max(0, discount)
        return 0
    
    @property
    def is_deal_available(self):
        """Check if current price meets the user's criteria"""
        return (
            self.product.current_price <= self.desired_price and
            self.current_discount_percent >= self.minimum_discount_percent
        )


class DealAlert(models.Model):
    """Model to track deal alerts sent to users"""
    
    tracked_product = models.ForeignKey(TrackedProduct, on_delete=models.CASCADE)
    alert_type = models.CharField(
        max_length=20,
        choices=[
            ('price_drop', 'Price Drop'),
            ('target_reached', 'Target Price Reached'),
            ('availability', 'Back in Stock'),
        ]
    )
    
    # Alert details
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Notification status
    email_sent = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)
    whatsapp_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'deal_alerts'
        verbose_name = 'Deal Alert'
        verbose_name_plural = 'Deal Alerts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tracked_product', 'created_at']),
            models.Index(fields=['alert_type']),
        ]
    
    def __str__(self):
        return f"{self.alert_type} alert for {self.tracked_product.product.name}"
