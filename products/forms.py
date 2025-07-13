# filepath: d:\Sandhya_H\Deal_Radar\products\forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
import logging

logger = logging.getLogger(__name__)

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            logger.warning(f"Attempt to register with existing email: {email}")
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            logger.info(f"New user created: {user.username} ({user.email})")
        return user

class TrackProductForm(forms.Form):
    target_price = forms.DecimalField(
        label="Target Price (£)",
        min_value=0,
        decimal_places=2,
        max_digits=10,
        required=True,
        error_messages={'invalid': 'Please enter a valid price (e.g., 79.99)'}
    )

    def clean_target_price(self):
        price = self.cleaned_data.get('target_price')
        if price is not None and price <= 0:
            logger.warning(f"Invalid target price entered: {price}")
            raise forms.ValidationError("Target price must be greater than 0.")
        return price

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'email_notifications',
            'whatsapp_notifications',
            'whatsapp_number',
            'notification_frequency',
        ]
        widgets = {
            'whatsapp_number': forms.TextInput(attrs={'placeholder': 'e.g. +447525121082'}),
        }