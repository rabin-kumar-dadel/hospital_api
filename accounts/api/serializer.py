from accounts.views import *
from rest_framework import serializers
from accounts.models import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate,login
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import Customuser, PatientProfile  # Adjust if needed

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

    

class PatientLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(style = {'input_type':'password'})



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

    

class DoctorRelatedAppoinmentSerializer(serializers.ModelSerializer):
    doctor = UserbasicSerializer(read_only = True)
    patient = UserbasicSerializer(read_only = True)
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'appointment_date', 'description', 'is_approved' ]



class ApponmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [ 'doctor', 'appointment_date', 'description']





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
    

