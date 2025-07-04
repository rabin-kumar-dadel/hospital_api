
from django.urls import path,include
from accounts.api.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'patientregisterapi' ,AppointmentPatientCreate, basename='patient_CRUD')

urlpatterns = [
    path('api/', include(router.urls)),
    

    # patient register api endpoint
    path('api/register/', PatientRegisterApiView.as_view(), name='patient_register'),

    # patient login api endpoint
    path('api/login/', PatientLoginView.as_view(), name='patient_register'),

]


