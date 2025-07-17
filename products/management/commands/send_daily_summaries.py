"""
Management command to send daily summary emails to users.

This command finds all users who have opted in for daily email notifications
and sends them a summary of their tracked products and recent price changes.

Usage:
    python manage.py send_daily_summaries
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.email_utils import send_daily_summary_email

class Command(BaseCommand):
    help = 'Send daily summary emails to users'

    def handle(self, *args, **options):
        self.stdout.write('📧 Sending daily summary emails...')

        # Get users who want daily summaries (based on profile settings)
        users_daily = User.objects.filter(
            userprofile__email_notifications=True,
            userprofile__notification_frequency='daily'
        )

        sent_count = 0
        total_users = users_daily.count()

        # Send summary email to each user
        for user in users_daily:
            if send_daily_summary_email(user):
                sent_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Daily summary sent to {user.email}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ No data to send for {user.email}')
                )

        self.stdout.write(f'📊 Processed {total_users} users')

        if sent_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'📧 {sent_count} daily summaries sent successfully!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ No daily summaries sent (no data or all disabled).')
            )

        self.stdout.write('✅ Daily summary emails completed.')