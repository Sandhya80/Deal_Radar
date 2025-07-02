from django.contrib import admin
from .models import Product

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
