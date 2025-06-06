from django.contrib import admin
from accounts.models import *

class Useradmin(admin.ModelAdmin):
    list_display = ['phone_number', 'first_name','is_active', 'is_patient', 'is_doctor', 'role', 'is_superuser', 'is_staff']
class patientadmin(admin.ModelAdmin):
    list_display = ['id', 'approve', 'patient_id']

admin.site.register(Customuser, Useradmin)


class apponmentadmin(admin.ModelAdmin):
    list_display = ['id']



admin.site.register(Appointment, apponmentadmin)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile, patientadmin)
