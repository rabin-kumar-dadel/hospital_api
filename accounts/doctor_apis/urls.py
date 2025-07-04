
from django.urls import path,include
from accounts.doctor_apis.views import *
from rest_framework.routers import DefaultRouter


# for the patient and doctor registration api
# router = DefaultRouter()


urlpatterns = [
    # path('api/', include(router.urls)),

    # doctor register api endpoint 
    path('api/register/',DoctorRegisterView.as_view(), name='doctor_register'),

    # doctor login api endpoint
    path('api/login/',DoctorLoginView.as_view(), name='doctor_register'),
    
    # patient code generate api endpoints
    path('patient/code/<pk>/', PatientCodeGenerateApi.as_view(), name='patient_code'),

    # doctor profile update api endpoints
    path('doctor/profile_update/', DoctorProfileApi.as_view(), name='doctor_profile_update'),

    # doctor appoinment show and approve api endpoints
    path('doctor/appointment/', DoctorApponmentView.as_view(), name='doc_appoint'),

    # patient approved appoinment api endpoints
    path('appoinment/<pk>/approve/', PatientApponmentApprove.as_view(), name='appoinment_approve'),

]


