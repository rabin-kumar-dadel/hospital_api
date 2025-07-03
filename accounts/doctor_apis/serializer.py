from accounts.views import *
from rest_framework import serializers
from accounts.models import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate,login



    


class PatientCodeAutoGenerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ['approve', 'patient_id']
        read_only_fields = ['patient_id']


    def validate(self, attrs):
        return super().validate(attrs)

 


class DoctorRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model = Customuser
        fields = ['phone_number', 'first_name', 'password1', 'password2']

    
    def validate(self, attrs):
        password1 = attrs['password1']
        password2 = attrs['password2']
        if password1 != password2:
            raise serializers.ValidationError("Passwords मिलेन।")
        validate_password(attrs['password1'])
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data['password1']
        user = Customuser(phone_number = validated_data['phone_number'], first_name = validated_data['first_name'])
        user.set_password(password)
        user.role = 'doctor'
        user.is_doctor = False
        user.is_active = False
        user.save()
        return  user
    

class DoctorloginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(style = {'input_type':'password'})
    


class DoctorprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['department', 'specialization']
        read_only_fields = ['user']

    


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
    

