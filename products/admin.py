from django.contrib import admin
from .models import Product, TrackedProduct, PriceAlert, UserProfile

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'current_price', 'target_price', 'category', 'site_name', 'is_active', 'created_at']
    list_filter = ['category', 'site_name', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'url', 'image_url')
        }),
        ('Pricing', {
            'fields': ('current_price', 'price', 'target_price')
        }),
        ('Categorization', {
            'fields': ('category', 'site_name')
        }),
        ('Status', {
            'fields': ('is_active', 'user')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TrackedProduct)
class TrackedProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'target_price', 'is_active', 'added_at']
    list_filter = ['is_active', 'added_at']
    search_fields = ['user__username', 'product__name']
    list_editable = ['is_active']
    raw_id_fields = ['user', 'product']

@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ['tracked_product', 'target_price', 'is_enabled', 'is_triggered', 'created_at']
    list_filter = ['is_enabled', 'is_triggered', 'created_at']
    search_fields = ['tracked_product__product__name', 'tracked_product__user__username']
    list_editable = ['is_enabled']
    readonly_fields = ['created_at', 'triggered_at']
    raw_id_fields = ['tracked_product']
    
    fieldsets = (
        ('Alert Configuration', {
            'fields': ('tracked_product', 'target_price', 'is_enabled')
        }),
        ('Status', {
            'fields': ('is_triggered', 'triggered_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'tracked_product__user', 'tracked_product__product'
        )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'created_at']
    list_filter = ['email_notifications', 'created_at']
    search_fields = ['user__username', 'user__email']
    list_editable = ['email_notifications']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['user']

# Optional: Custom admin site configuration
admin.site.site_header = "Deal Radar Administration"
admin.site.site_title = "Deal Radar Admin"
admin.site.index_title = "Welcome to Deal Radar Administration"
