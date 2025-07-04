from accounts.views import *
from rest_framework import serializers
from accounts.models import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate,login

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


    


class PatientCodeAutoGenerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ['approve', 'patient_id']
        read_only_fields = ['patient_id']


    def validate(self, attrs):
        return super().validate(attrs)


# doctor registration serializer
class DoctorRegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()
    phone_number = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            'full_name','phone_number', 'password', 'confirm_password', 'specialization', 'license_number',
            'experience_years', 'hospital_location', 'department', 
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")

        # Optional: Validate phone number uniqueness here
        if Customuser.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError("Phone number already registered.")
        return data

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        phone_number = validated_data.pop('phone_number')
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')

        first_name = full_name.strip()

        # Create user — better to use your custom user manager's create_user method
        user = Customuser.objects.create_user(
            phone_number=phone_number,
            first_name = first_name,
            is_active=False,        # depends on your workflow
            is_doctor=False,         # mark as doctor
            role='doctor',          # make sure this is a valid role choice
        )
        user.set_password(password)
        user.save()

        # Create doctor profile linked to user
        doctor = DoctorProfile.objects.create(user=user,
                                              full_name = full_name, 
                                              **validated_data)
        return doctor


# doctor login serializer
class DoctorLoginSerializer(serializers.Serializer):
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
        if not user.is_doctor:
            raise serializers.ValidationError("Access denied: Not a doctor.")

        token = get_tokens_for_user(user)

        return {
            'refresh': str(token),
            'access': str(token),
            'phone_number': user.phone_number,
        }


# doctor profile serializer
class DoctorprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['department', 'specialization']
        read_only_fields = ['user']

    
    
# doctor related apponments serializer
class DoctorRelatedAppoinmentSerializer(serializers.ModelSerializer):
    doctor = UserbasicSerializer(read_only = True)
    patient = UserbasicSerializer(read_only = True)
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'appointment_date', 'description', 'is_approved' ]


# all approved appoinments by doctor
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
