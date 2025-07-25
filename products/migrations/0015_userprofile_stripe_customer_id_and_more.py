# Generated by Django 5.0.6 on 2025-07-14 23:15

# Migration to add Stripe customer ID and subscription status to UserProfile.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_userprofile_stripe_subscription_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='subscription_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='stripe_subscription_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
