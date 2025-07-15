from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import logging
from .whatsapp_utils import send_whatsapp_alert
from cloudinary.models import CloudinaryField
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

logger = logging.getLogger(__name__)

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
    
    name = models.CharField(max_length=255)
    url = models.URLField()
    site_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
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
        logger.debug(f"Saving product: {self.name} (Price: {self.price}, Current Price: {self.current_price})")
        super().save(*args, **kwargs)

    def get_category_display_with_emoji(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)

class UserProfile(models.Model):
    """User profile for notification preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    whatsapp_notifications = models.BooleanField(default=False)  # Add this
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)  # Add this
    notification_frequency = models.CharField(
        max_length=10,
        choices=[
            ('immediate', 'Immediate'),
            ('daily', 'Daily Summary'),
            ('weekly', 'Weekly Summary'),
        ],
        default='immediate'
    )
    subscription_plan = models.CharField(
        max_length=20,
        choices=[('free', 'Free'), ('basic', 'Basic'), ('premium', 'Premium')],
        default='free'
    )
    # Stripe fields:
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    subscription_status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        logger.info(f"Created UserProfile for new user: {instance.username}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
        logger.debug(f"Saved UserProfile for user: {instance.username}")
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
        logger.warning(f"UserProfile did not exist for user: {instance.username}, created new one.")

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
    tracked_product = models.ForeignKey('TrackedProduct', on_delete=models.CASCADE)
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_triggered = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=True)
    triggered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['tracked_product', 'target_price']
    
    def __str__(self):
        return f"Alert: {self.tracked_product.product.name} - £{self.target_price}"

    def check_price_drop(self):
        current_price = self.tracked_product.product.current_price
        logger.debug(f"Checking price drop for {self.tracked_product.product.name}: Current {current_price}, Target {self.target_price}")
        return current_price <= self.target_price

    def trigger_alert(self, current_price):
        user_profile = self.tracked_product.user.userprofile
        if not self.is_triggered and self.is_enabled:
            self.is_triggered = True
            self.triggered_at = timezone.now()
            self.save()
            # WhatsApp alert
            if user_profile.whatsapp_notifications and user_profile.whatsapp_number:
                message = (
                    f"Deal Radar Alert!\n\n"
                    f"The product '{self.tracked_product.product.name}' has dropped to £{current_price}.\n"
                    f"Your target price was £{self.target_price}.\n"
                    f"View: {self.tracked_product.product.url}"
                )
                send_whatsapp_alert(user_profile.whatsapp_number, message)
            # (Optional) Email alert logic can go here as well
            return True
        return False