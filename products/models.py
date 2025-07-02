from django.db import models
from django.urls import reverse

class Product(models.Model):
    """Phase 2: Simple product model for basic tracking"""
    name = models.CharField(max_length=200)
    url = models.URLField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    site_name = models.CharField(max_length=100, blank=True)  # Amazon, eBay, etc.
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - £{self.current_price}"

    class Meta:
        ordering = ['-created_at']
