from accounts.views import *
from rest_framework import serializers
from accounts.models import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate,login
from rest_framework.exceptions import AuthenticationFailed

# token authentication
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Authorize user registration serializer
class AuthorizedRegisterSerializer(serializers.Serializer):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('admin', 'Admin'),
    )

    full_name = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    # Optional fields for doctor/nurse profiles
    specialization = serializers.CharField(required=False)
    license_number = serializers.CharField(required=False)
    experience_years = serializers.IntegerField(required=False)
    hospital_location = serializers.CharField(required=False)
    department = serializers.CharField(required=False)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")

        if Customuser.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError("Phone number already registered.")

     
        return data

    def create(self, validated_data):
        role = validated_data.pop('role')
        full_name = validated_data.pop('full_name')
        phone_number = validated_data.pop('phone_number')
        password = validated_data.pop('password')
        validated_data.pop('confirm_password', None)

        first_name = full_name.strip()

        user = Customuser.objects.create_user(
            phone_number=phone_number,
            first_name = first_name,
            is_doctor=(role == 'doctor'),
            is_nurse=(role == 'nurse'),
            is_admin=(role == 'admin'),
            is_active=True,
        )
        user.set_password(password)
        user.save()

        if role == 'doctor':
            return DoctorProfile.objects.create(user=user, full_name=full_name, **validated_data)
        elif role == 'nurse':
            return NurseProfile.objects.create(user=user, full_name=full_name, **validated_data)

        return user  # for admin, return user only



# Authorize user login serializer
class AuthorizedLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get("phone_number")
        password = data.get("password")

        user = authenticate(phone_number=phone, password=password)

        if not user:
            raise AuthenticationFailed("Invalid phone number or password.")

        if not user.is_active:
            raise AuthenticationFailed("Account not approved by admin yet.")

        # Check user role
        if user.is_doctor:
            role = "doctor"
        elif user.is_nurse:
            role = "nurse"
        elif user.is_admin:
            role = "admin"
        else:
            raise AuthenticationFailed("Unauthorized role.")

        # Generate tokens
        refresh = get_tokens_for_user(user)

        return {
            "access": str(refresh),
            "refresh": str(refresh),
            "role": role,
            "user_id": user.id,
            "phone_number": user.phone_number,
            "first_name": user.first_name
        }
