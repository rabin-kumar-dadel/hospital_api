from accounts.views import *
from rest_framework import serializers
from accounts.models import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate,login
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import Customuser, PatientProfile 
from rest_framework_simplejwt.tokens import RefreshToken

# token authentication
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# patient registration serializer
class PatientRegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = PatientProfile
        fields = [
            'phone_number', 'first_name', 'password', 'confirm_password',
            'middle_name', 'lastname', 'date_of_birth', 'gender', 'phone',
            'province', 'district', 'local_level', 'ward_number', 'street_address'
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if Customuser.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError("Phone number already registered.")
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        # Extract and remove user-related fields
        phone_number = validated_data.pop('phone_number')
        first_name = validated_data.pop('first_name')
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')

        # Create user
        user = Customuser.objects.create_user(
            phone_number=phone_number,
            first_name=first_name,
            is_active=False,
            is_patient=True,
            role='patient',
        )
        user.set_password(password)
        user.save()

        # Create profile
        patient = PatientProfile.objects.create(user=user, **validated_data)
        return patient

    

# patient Login Serializer
class PatientLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), phone_number=phone_number, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("Account inactive.")
        if not user.is_patient:
            raise serializers.ValidationError("Access denied: Not a patient.")

        token = get_tokens_for_user(user)

        return {
            'refresh': str(token),
            'access': str(token),
        }


# patient code generator
class PatientCodeAutoGenerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ['approve', 'patient_id']
        read_only_fields = ['patient_id']


    def validate(self, attrs):
        return super().validate(attrs)

 




    


class UserbasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ['first_name']

    
# doctor related appointment serializer
class DoctorRelatedAppoinmentSerializer(serializers.ModelSerializer):
    doctor = UserbasicSerializer(read_only = True)
    patient = UserbasicSerializer(read_only = True)
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'appointment_date', 'description', 'is_approved' ]


# all appointment
class ApponmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [ 'doctor', 'appointment_date', 'description']




# approved appointment by doctor
class ApproveApponmentByDoctor(serializers.ModelSerializer):
    is_approved = serializers.BooleanField(write_only = True)
    class Meta:
        model = Appointment
        fields = ['is_approved']

    def validate(self, attrs):
        instance = self.instance
        if instance.is_approved:
            raise serializers.ValidationError('Appoinment is already approved ')
        
        if instance.doctor != self.context['request'].user:
            raise serializers.ValidationError('Doctor does not have permission to approve this')
        
        return attrs
    
    def update(self, instance, validated_data):
        instance = self.instance
        instance.is_approved = True
        instance.save()
        return instance
    

