from accounts.forms import *
from accounts.mixins import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from accounts.doctor_apis.serializer import *
from rest_framework.response import Response
from accounts.api.serializer import *
from rest_framework import viewsets
from rest_framework.mixins import *
from rest_framework.generics import *
from accounts.api.serializer import PatientRegisterSerializer,PatientLoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,login
from rest_framework.decorators import action
from accounts.permission import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }







class PatientCodeGenerateApi(UpdateAPIView):
    permission_classes = [IsAuthenticated, isDoctor]
    queryset = PatientProfile.objects.all()
    serializer_class = PatientCodeAutoGenerateSerializer
    

class PatientApponmentApprove(UpdateAPIView):
    permission_classes = [IsAuthenticated, isDoctor]
    queryset = Appointment.objects.all()
    serializer_class = ApproveApponmentByDoctor





class DoctorRegisterView(CreateAPIView):
    serializer_class = DoctorRegisterSerializer
    permission_classes = [AllowAny]


# doctorprofile completion 


class DoctorProfileApi(RetrieveUpdateAPIView):
    serializer_class = DoctorprofileSerializer
    permission_classes = [IsAuthenticated, isDoctor]
    throttle_classes = [UserRateThrottle]
    
    def get_object(self):
        return self.request.user.doctorprofile
    
  
    
    

class DoctorApponmentView(ListAPIView):
    serializer_class = DoctorRelatedAppoinmentSerializer
    permission_classes = [IsAuthenticated, isDoctor]
    
    def get_queryset(self):
        return Appointment.objects.select_related('doctor').filter(doctor = self.request.user)
    

class AppointmentPatientCreate(viewsets.ModelViewSet):
    serializer_class = ApponmentSerializer
    permission_classes = [IsAuthenticated, ispatient]
    queryset = Appointment.objects.all()
    throttle_classes = [UserRateThrottle]


    def perform_create(self, serializer):
        serializer.save(patient = self.request.user)
        



