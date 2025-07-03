from django.contrib import admin
from .models import Product, UserProfile, TrackedProduct, PriceAlert

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'current_price', 'site_name', 'category', 'created_at']
    list_filter = ['site_name', 'category', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    # Add custom actions
    actions = ['update_prices']
    
    def update_prices(self, request, queryset):
        # Manual price update functionality
        self.message_user(request, f"Updated {queryset.count()} products")
    update_prices.short_description = "Update selected product prices"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'email_notifications']
    list_filter = ['created_at', 'email_notifications']
    search_fields = ['user__username', 'user__email']

@admin.register(TrackedProduct)
class TrackedProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'target_price', 'added_at', 'is_active']
    list_filter = ['is_active', 'added_at']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['added_at']

@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ['tracked_product', 'alert_threshold', 'alert_type', 'is_enabled']
    list_filter = ['alert_type', 'is_enabled', 'created_at']
    search_fields = ['tracked_product__product__name', 'tracked_product__user__username']
