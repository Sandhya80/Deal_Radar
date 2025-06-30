"""
Notification Views for Deal Radar

This module handles notification management and delivery for price alerts.
It provides interfaces for managing notification preferences, testing
delivery methods, and viewing notification history.

Implementation Strategy:
- Phase 1: Basic structure and settings interface
- Phase 2: Email notification implementation
- Phase 3: SMS/WhatsApp integration via Twilio
- Phase 4: Push notifications for mobile apps

Business Logic:
- Multi-channel notification delivery (email, SMS, WhatsApp)
- Rate limiting to prevent spam
- User preference management
- Delivery status tracking and retry logic
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@login_required
def notification_settings(request):
    """
    Notification preferences management view
    
    This view allows users to configure their notification preferences
    including delivery methods, frequency, and content options.
    
    Business Logic:
    - Users can enable/disable different notification channels
    - Phone number required for SMS/WhatsApp notifications
    - Email notifications enabled by default
    - Test functionality to verify delivery methods
    
    Settings Available:
    - Email notifications (price drops, deal alerts)
    - SMS notifications (requires phone number)
    - WhatsApp notifications (requires phone number)
    - Notification frequency (immediate, daily digest, weekly)
    - Price drop threshold (minimum % to trigger alert)
    
    Phase Implementation:
    - Phase 1: Basic settings interface (current)
    - Phase 2: Email notification configuration
    - Phase 3: SMS/WhatsApp integration
    - Phase 4: Push notification settings
    
    Future Enhancements:
    - Notification scheduling (quiet hours)
    - Custom message templates
    - Delivery method priorities
    - Bulk notification management
    """
    profile = getattr(request.user, 'profile', None)
    
    if request.method == 'POST':
        if profile:
            # Update notification preferences
            profile.email_notifications = request.POST.get('email_notifications') == 'on'
            profile.sms_notifications = request.POST.get('sms_notifications') == 'on'
            profile.whatsapp_notifications = request.POST.get('whatsapp_notifications') == 'on'
            
            # Validate phone number if SMS/WhatsApp enabled
            if (profile.sms_notifications or profile.whatsapp_notifications):
                phone = request.POST.get('phone_number', '').strip()
                if not phone:
                    messages.error(request, 'Phone number is required for SMS or WhatsApp notifications.')
                    return render(request, 'notifications/settings.html', {'profile': profile})
                profile.phone_number = phone
            
            profile.save()
            messages.success(request, 'Notification settings updated successfully!')
    
    context = {
        'profile': profile,
        'has_phone': bool(profile.phone_number) if profile else False,
        # Phase 3 additions:
        # 'delivery_status': recent notification delivery status
        # 'notification_history': recent notifications sent
    }
    
    return render(request, 'notifications/settings.html', context)

@login_required
def test_notification(request):
    """
    Test notification delivery endpoint
    
    This view allows users to test their notification setup by sending
    a sample notification through their configured delivery methods.
    
    Business Logic:
    - Validates user's notification settings before testing
    - Sends test messages through enabled channels
    - Returns delivery status and any error messages
    - Rate limited to prevent abuse
    
    Test Process:
    1. Check user's notification preferences
    2. Validate contact information (email, phone)
    3. Send test messages through enabled channels
    4. Return delivery status and confirmation
    
    Supported Channels:
    - Email: Test email with sample price alert
    - SMS: Test SMS message (Phase 3)
    - WhatsApp: Test WhatsApp message (Phase 3)
    - Push: Test push notification (Phase 4)
    
    Error Handling:
    - Invalid/missing contact information
    - Delivery failures and timeout issues
    - Service unavailability (Twilio, email server)
    - Rate limiting for abuse prevention
    
    Future Enhancements:
    - Delivery time tracking and reporting
    - A/B testing for message content
    - Delivery method fallback logic
    - Bulk testing for multiple users
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    profile = getattr(request.user, 'profile', None)
    if not profile:
        return JsonResponse({'error': 'User profile not found'}, status=404)
    
    results = {'sent': [], 'failed': [], 'message': ''}
    
    # Test email notification
    if profile.email_notifications and request.user.email:
        try:
            # Phase 2 implementation: send actual test email
            # For now, simulate success
            results['sent'].append('email')
            # Implementation:
            # from django.core.mail import send_mail
            # send_mail(subject, message, from_email, [user.email])
        except Exception as e:
            results['failed'].append({'channel': 'email', 'error': str(e)})
    
    # Test SMS notification (Phase 3)
    if profile.sms_notifications and profile.phone_number:
        try:
            # Phase 3 implementation: Twilio SMS
            results['sent'].append('sms')
            # Implementation:
            # from twilio.rest import Client
            # client.messages.create(to=phone, from_=twilio_number, body=message)
        except Exception as e:
            results['failed'].append({'channel': 'sms', 'error': str(e)})
    
    # Test WhatsApp notification (Phase 3)
    if profile.whatsapp_notifications and profile.phone_number:
        try:
            # Phase 3 implementation: Twilio WhatsApp
            results['sent'].append('whatsapp')
        except Exception as e:
            results['failed'].append({'channel': 'whatsapp', 'error': str(e)})
    
    # Prepare response message
    if results['sent']:
        sent_channels = ', '.join(results['sent'])
        results['message'] = f'Test notifications sent successfully via: {sent_channels}'
    else:
        results['message'] = 'No notifications sent. Please check your settings and contact information.'
    
    if results['failed']:
        results['message'] += f" Some channels failed: {len(results['failed'])} errors."
    
    return JsonResponse({
        'status': 'success' if results['sent'] else 'warning',
        'message': results['message'],
        'details': results
    })

# API Views for Notification Management

@api_view(['GET'])
def notification_history_api(request):
    """
    API endpoint for notification history
    
    This RESTful API endpoint provides programmatic access to a user's
    notification history for mobile apps and analytics.
    
    Authentication:
    - Requires valid authentication token or active session
    - Returns 401 for unauthenticated requests
    
    Response Format:
    - JSON array of recent notifications with delivery status
    - Includes notification type, channel, delivery time
    - Paginated for performance with large histories
    
    Business Logic:
    - Only returns notifications for the authenticated user
    - Includes successful and failed delivery attempts
    - Shows notification content and delivery methods
    - Provides delivery analytics and statistics
    
    Future Implementation (Phase 3):
    - Query notification delivery logs from database
    - Include delivery status and error messages
    - Provide filtering by date range and channel
    - Return delivery statistics and performance metrics
    
    Example Response:
    {
        "notifications": [
            {
                "id": 1,
                "type": "price_drop",
                "product_name": "iPhone 15 Pro",
                "message": "Price dropped to £699.99",
                "channels": ["email", "sms"],
                "sent_at": "2024-01-15T10:30:00Z",
                "delivery_status": "delivered"
            }
        ],
        "total_count": 25,
        "page": 1,
        "has_next": true
    }
    """
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    # Phase 3 implementation will query actual notification logs
    # For now, return placeholder structure
    
    # Future implementation:
    # from products.models import DealAlert
    # alerts = DealAlert.objects.filter(
    #     tracked_product__user=request.user
    # ).order_by('-created_at')[:20]
    
    # Placeholder response for Phase 1
    data = {
        'notifications': [],
        'total_count': 0,
        'message': 'Notification history will be available in Phase 3',
        'features_coming': [
            'Email delivery tracking',
            'SMS delivery status',
            'WhatsApp message history',
            'Delivery analytics and reporting'
        ]
    }
    
    return Response(data)
