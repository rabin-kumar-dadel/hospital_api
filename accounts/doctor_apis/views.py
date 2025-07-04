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




# patient code generator by doctor
class PatientCodeGenerateApi(UpdateAPIView):
    permission_classes = [IsAuthenticated, isDoctor]
    queryset = PatientProfile.objects.all()
    serializer_class = PatientCodeAutoGenerateSerializer
    
# approved appoinment of patient
class PatientApponmentApprove(UpdateAPIView):
    permission_classes = [IsAuthenticated, isDoctor]
    queryset = Appointment.objects.all()
    serializer_class = ApproveApponmentByDoctor




# doctor register view
class DoctorRegisterView(CreateAPIView):
    serializer_class = DoctorRegisterSerializer
    permission_classes = [AllowAny]


# doctor login veiw
class DoctorLoginView(GenericAPIView):
    serializer_class = DoctorLoginSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Adding custom message to response
        return Response({
            "message": "Doctor logged in successfully.",
            "refresh": data['refresh'],
            "access": data['access'],
        }, status=status.HTTP_200_OK)


# doctor profile update view
class DoctorProfileApi(RetrieveUpdateAPIView):
    serializer_class = DoctorprofileSerializer
    permission_classes = [IsAuthenticated, isDoctor]
    throttle_classes = [UserRateThrottle]
    
    def get_object(self):
        return self.request.user.doctorprofile
    
  
    
    
# doctor appoinment view
class DoctorApponmentView(ListAPIView):
    serializer_class = DoctorRelatedAppoinmentSerializer
    permission_classes = [IsAuthenticated, isDoctor]
    
    def get_queryset(self):
        return Appointment.objects.select_related('doctor').filter(doctor = self.request.user)
    
