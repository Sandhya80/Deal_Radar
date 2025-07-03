from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    """Product model for tracking items across e-commerce sites"""
    name = models.CharField(max_length=200)
    url = models.URLField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    site_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """Extended user profile for Phase 3"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    email_notifications = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class TrackedProduct(models.Model):
    """User's personally tracked products - Phase 3"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracked_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    target_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('user', 'product')
    
    def __str__(self):
        return f"{self.user.username} tracking {self.product.name}"

class PriceAlert(models.Model):
    """Price alert settings for tracked products - Phase 3"""
    tracked_product = models.OneToOneField(TrackedProduct, on_delete=models.CASCADE)
    alert_threshold = models.DecimalField(max_digits=10, decimal_places=2)
    alert_type = models.CharField(max_length=20, choices=[
        ('below', 'Alert when price goes below'),
        ('above', 'Alert when price goes above'),
        ('change', 'Alert on any price change')
    ], default='below')
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Alert for {self.tracked_product.product.name} at £{self.alert_threshold}"
