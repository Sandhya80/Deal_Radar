from django.contrib import admin
from .models import Product, UserProfile, TrackedProduct, PriceAlert

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'current_price', 'price', 'target_price', 'category', 'site_name', 'user', 'is_active', 'created_at']
    list_filter = ['category', 'site_name', 'is_active', 'created_at', 'user']
    search_fields = ['name', 'description', 'site_name', 'user__username']
    list_editable = ['is_active', 'current_price', 'price', 'target_price']
    list_per_page = 25
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'user'),
            'description': 'Basic product information and categorization'
        }),
        ('Pricing', {
            'fields': ('current_price', 'price', 'target_price'),
            'description': 'Current price, compatibility price, and target price'
        }),
        ('Links & Media', {
            'fields': ('url', 'image_url', 'site_name'),
            'description': 'Product URL, image, and source site'
        }),
        ('Settings', {
            'fields': ('is_active',),
            'description': 'Product visibility and status'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'description': 'Creation and modification times',
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def save_model(self, request, obj, form, change):
        # If no user is assigned, assign the current admin user
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'preferred_categories_display', 'created_at']
    list_filter = ['email_notifications', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    list_editable = ['email_notifications']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Preferences', {
            'fields': ('email_notifications', 'preferred_categories')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def preferred_categories_display(self, obj):
        """Display preferred categories in a readable format"""
        if obj.preferred_categories:
            return obj.preferred_categories[:50] + "..." if len(obj.preferred_categories) > 50 else obj.preferred_categories
        return "None"
    preferred_categories_display.short_description = 'Preferred Categories'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(TrackedProduct)
class TrackedProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'target_price', 'is_active', 'added_at']
    list_filter = ['is_active', 'added_at', 'product__category', 'product__site_name']
    search_fields = ['user__username', 'product__name', 'product__description']
    list_editable = ['is_active', 'target_price']
    list_per_page = 25
    ordering = ['-added_at']
    
    fieldsets = (
        ('Tracking Information', {
            'fields': ('user', 'product', 'target_price', 'is_active')
        }),
        ('Timeline', {
            'fields': ('added_at',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['added_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'product')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            kwargs["queryset"] = Product.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ['tracked_product', 'alert_type', 'alert_threshold', 'is_enabled', 'created_at']
    list_filter = ['alert_type', 'is_enabled', 'created_at', 'tracked_product__product__category']
    search_fields = ['tracked_product__product__name', 'tracked_product__user__username']
    list_editable = ['is_enabled', 'alert_threshold']
    list_per_page = 25
    ordering = ['-created_at']
    
    fieldsets = (
        ('Alert Configuration', {
            'fields': ('tracked_product', 'alert_type', 'alert_threshold', 'is_enabled')
        }),
        ('Timeline', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('tracked_product__product', 'tracked_product__user')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tracked_product":
            kwargs["queryset"] = TrackedProduct.objects.filter(is_active=True).select_related('product', 'user')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Optional: Custom admin site configuration
admin.site.site_header = "Deal Radar Administration"
admin.site.site_title = "Deal Radar Admin"
admin.site.index_title = "Welcome to Deal Radar Administration"
