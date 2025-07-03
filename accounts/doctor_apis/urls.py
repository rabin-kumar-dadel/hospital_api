"""
URL configuration for hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from accounts.doctor_apis.views import *
from rest_framework.routers import DefaultRouter


# for the patient and doctor registration api
router = DefaultRouter()
router.register(r'patientregisterapi' ,AppointmentPatientCreate, basename='patient_CRUD')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/',DoctorRegisterView.as_view(), name='doctor_register'),
    
    # patient code generate api 
    path('patient/code/<pk>/', PatientCodeGenerateApi.as_view(), name='patient_code'),

    # doctor profile update api
    path('doctor/profile_update/', DoctorProfileApi.as_view(), name='doctor_profile_update'),

    # doctor appoinment show and approve api
    path('doctor/appointment/', DoctorApponmentView.as_view(), name='doc_appoint'),
    path('appoinment/<pk>/approve/', PatientApponmentApprove.as_view(), name='appoinment_approve'),

]


