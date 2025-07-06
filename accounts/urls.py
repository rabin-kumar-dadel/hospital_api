
from django.urls import path
from accounts.views import *

urlpatterns = [
    path('', home, name='home' ),
    path('doctor/register/', Doctorview.as_view(), name='doctor_register'),
    path('success/', success, name='success'),
    path('doctor/login/', Doctor_login_view.as_view(), name='doctor_login'),
    path('doctor/dashboard/', doctordashboardview.as_view(), name='doctor_dash'),
    path('doctor/logout/', doctorlogoutview.as_view(), name='doctor_logout'),

    path('doctor/approve/<pk>/', approveappoint.as_view(), name = 'approve_appointment'),

    path('appoint/delete/<int:pk>/', AppointDeleteView.as_view(), name='appoint_delete'),

    path('doctor/edit-profile/', DoctorProfileUpdatevIEW.as_view(), name='edit_profile'),


    # for the patient urls

    path('patient/register/',Patientview.as_view(), name='patient_register'),

    path('patient/login/',Patient_login_view.as_view(), name='patient_login'),

    path('patient/dashboard/',patientdashboardview.as_view(), name='patient_dashboard'),

    path('patient/logout/',patientlogoutview.as_view(), name='patient_logout'),

    path('patient/appoint/', PatientAppointmentvIEW.as_view(), name='patient_appoint'),
    

# password reset api endpoints
    path('api/password-reset/', RequestOTPView.as_view(), name='request-otp'),
    path('api/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('api/reset-password/', ResetPasswordView.as_view(), name='reset-password'),


]
