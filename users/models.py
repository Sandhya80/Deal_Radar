from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

class UserProfile(models.Model):
    """
    Extended user profile for Deal Radar users
    
    This model extends Django's built-in User model with Deal Radar-specific
    functionality without modifying the core User table.
    
    Business Logic:
    - Manages subscription tiers and limits
    - Stores notification preferences
    - Tracks subscription status and billing
    
    Design Pattern:
    - OneToOne relationship with User (Profile Pattern)
    - Separates authentication from business logic
    - Enables easy subscription tier management
    """
    
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # Contact preferences for notifications
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    
    # Notification preferences - controls how user receives alerts
    email_notifications = models.BooleanField(default=True)     # Email alerts enabled
    sms_notifications = models.BooleanField(default=False)      # SMS alerts (requires phone + Twilio)
    whatsapp_notifications = models.BooleanField(default=False) # WhatsApp alerts (requires phone + Twilio)
    
    # Subscription status and billing management
    is_premium = models.BooleanField(default=False)             # Premium subscription status
    subscription_end_date = models.DateTimeField(blank=True, null=True)  # When subscription expires
    
    # Business rule enforcement - subscription tier limits
    max_tracked_products = models.IntegerField(default=3)       # Free: 3, Premium: unlimited (999)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def can_track_more_products(self):
        """
        Check if user can track more products based on their subscription
        
        Business Logic:
        - Free users: limited to 3 tracked products
        - Premium users: unlimited tracking (enforced by high limit)
        
        Returns:
            bool: True if user can add more products to tracking
        """
        from products.models import TrackedProduct
        current_count = TrackedProduct.objects.filter(user=self.user).count()
        return current_count < self.max_tracked_products
