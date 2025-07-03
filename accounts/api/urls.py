
from django.urls import path,include
from accounts.api.views import *
from rest_framework.routers import DefaultRouter


# for the patient and doctor registration api
router = DefaultRouter()
router.register(r'' ,AuthViewSet, basename='patient_login' )
router.register(r'patientregisterapi' ,AppointmentPatientCreate, basename='patient_CRUD')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', PatientRegisterApiView.as_view(), name='patient_register'),

]


