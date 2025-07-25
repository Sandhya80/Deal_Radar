# Generated by Django 5.2.3 on 2025-07-02 23:25

# Migration to reintroduce TrackedProduct, PriceAlert, and UserProfile models.
# Adds fields for tracking, alerts, and user preferences.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_dealalert_tracked_product_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Create TrackedProduct model for user-product tracking
        migrations.CreateModel(
            name='TrackedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracked_products', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'product')},
            },
        ),
        # Create PriceAlert model for price alert logic
        migrations.CreateModel(
            name='PriceAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert_threshold', models.DecimalField(decimal_places=2, max_digits=10)),
                ('alert_type', models.CharField(choices=[('below', 'Alert when price goes below'), ('above', 'Alert when price goes above'), ('change', 'Alert on any price change')], default='below', max_length=20)),
                ('is_enabled', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tracked_product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.trackedproduct')),
            ],
        ),
        # Create UserProfile model for user preferences
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email_notifications', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
