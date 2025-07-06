# serializers.py
from rest_framework import serializers
from accounts.models import Customuser, OtpVerification
import random

from twilio.rest import Client
from django.conf import settings
import random
from twilio.rest import Client
from django.conf import settings
from rest_framework import serializers
from .models import Customuser, OtpVerification


class RequestOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, phone):
        if not Customuser.objects.filter(phone_number=phone).exists():
            raise serializers.ValidationError("No user with this phone number.")
        return phone

    def format_phone_to_e164(self, phone):
        phone = phone.strip()
        if phone.startswith('+'):
            return phone
        return '+977' + phone

    def create(self, validated_data):
        phone = validated_data['phone_number']
        otp = str(random.randint(100000, 999999))

        # Save OTP to the DB
        OtpVerification.objects.create(phone_number=phone, otp=otp)

        # Format phone to E.164
        formatted_phone = self.format_phone_to_e164(phone)

        # Twilio credentials from settings.py
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        from_number = settings.TWILIO_PHONE_NUMBER

        client = Client(account_sid, auth_token)

        # Send SMS with formatted phone number
        message = client.messages.create(
            body=f"Your password reset OTP is: {otp} Please do not share with Anyone. Thankyou from The Health",
            from_=from_number,
            to=formatted_phone
        )

        return validated_data

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, data):
        phone = data['phone_number']
        otp = data['otp']
        try:
            otp_obj = OtpVerification.objects.filter(phone_number=phone, otp=otp).latest('created_at')
        except OtpVerification.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP.")

        if otp_obj.is_expired():
            raise serializers.ValidationError("OTP has expired.")

        otp_obj.is_verified = True
        otp_obj.save()
        return data
    

class ResetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data['phone_number']
        try:
            otp_obj = OtpVerification.objects.filter(phone_number=phone, is_verified=True).latest('created_at')
        except OtpVerification.DoesNotExist:
            raise serializers.ValidationError("OTP not verified for this number.")

        if otp_obj.is_expired():
            raise serializers.ValidationError("OTP expired.")

        return data

    def save(self):
        phone = self.validated_data['phone_number']
        password = self.validated_data['new_password']
        user = Customuser.objects.get(phone_number=phone)
        user.set_password(password)
        user.save()
        OtpVerification.objects.filter(phone_number=phone).delete()  # Cleanup
        return user




























