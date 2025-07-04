from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    """Product model for tracking items across e-commerce sites"""
    CATEGORY_CHOICES = [
        ('electronics', '📱 Electronics'),
        ('clothing', '👕 Fashion & Clothing'),
        ('home', '🏠 Home & Garden'),
        ('books', '📚 Books'),
        ('sports', '⚽ Sports & Outdoors'),
        ('beauty', '💄 Beauty & Health'),
        ('gaming', '🎮 Gaming'),
        ('automotive', '🚗 Automotive'),
        ('toys', '🧸 Toys & Games'),
    ]
    
    name = models.CharField(max_length=200)
    url = models.URLField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Add this for compatibility
    target_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    site_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='electronics')
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Keep current_price and price in sync
        if self.current_price and not self.price:
            self.price = self.current_price
        elif self.price and not self.current_price:
            self.current_price = self.price
        super().save(*args, **kwargs)
    
    def get_category_display_with_emoji(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)

class UserProfile(models.Model):
    """Extended user profile for Phase 3"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    preferred_categories = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class TrackedProduct(models.Model):
    """Products that users are tracking for price changes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracked_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='tracked_by')
    target_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f"{self.user.username} tracking {self.product.name}"

class PriceAlert(models.Model):
    """Price alerts for tracked products"""
    ALERT_TYPES = [
        ('price_drop', 'Price Drop'),
        ('target_reached', 'Target Price Reached'),
        ('stock_available', 'Back in Stock'),
    ]
    
    tracked_product = models.ForeignKey(TrackedProduct, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    alert_threshold = models.DecimalField(max_digits=10, decimal_places=2)
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Alert for {self.tracked_product.product.name}"
