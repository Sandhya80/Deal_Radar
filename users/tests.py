from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile

# Create your tests here.

class UserProfileTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_profile_creation(self):
        """Test that user profile is created correctly"""
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.user, self.user)
        self.assertTrue(profile.email_notifications)
        self.assertFalse(profile.sms_notifications)
        self.assertFalse(profile.whatsapp_notifications)
        self.assertEqual(profile.max_tracked_products, 3)
    
    def test_can_track_more_products(self):
        """Test the can_track_more_products property"""
        profile = UserProfile.objects.create(user=self.user)
        # Initially should be able to track more (0 < 3)
        self.assertTrue(profile.can_track_more_products)
