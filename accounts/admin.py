from django.contrib import admin
from accounts.models import *

class Useradmin(admin.ModelAdmin):
    list_display = ['phone_number', 'first_name','is_active', 'is_patient', 'is_doctor', 'role', 'is_superuser', 'is_staff']
class patientadmin(admin.ModelAdmin):
    list_display =  ['user', 'middle_name', 'lastname', 'date_of_birth', 'gender', 'phone',
            'province', 'district', 'local_level', 'ward_number', 'street_address','patient_id','approve']

admin.site.register(Customuser, Useradmin)


class apponmentadmin(admin.ModelAdmin):
    list_display = ['id']



admin.site.register(Appointment, apponmentadmin)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile, patientadmin)

class NurseprofileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'license_number', 'experience_years', 'hospital_location']


# register NurseProfile
admin.site.register(NurseProfile, NurseprofileAdmin)

# register OtpVerification
admin.site.register(OtpVerification)
