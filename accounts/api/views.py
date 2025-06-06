from accounts.forms import *
from accounts.mixins import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from accounts.api.serializer import *
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



class PatientRegisterApiView(CreateAPIView):
    queryset = Customuser.objects.none()
    serializer_class = PatientRegisterSerializer
    permission_classes = [AllowAny]



class AuthViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['post'], url_path='patient/login')
    def patient_login(self, request):
        serializer = PatientLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']

        # Authenticate user
        user = authenticate(username=phone_number, password=password)
        if user is not None:
            login(request, user)  # Optional: only needed if using Django sessions
            token = get_tokens_for_user(user)

            return Response({
                'message': 'Login सफल भयो',
                'token': token
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PatientCodeGenerateApi(UpdateAPIView):
    permission_classes = [IsAuthenticated, isDoctor]
    queryset = PatientProfile.objects.all()
    serializer_class = PatientCodeAutoGenerateSerializer
    

class PatientApponmentApprove(UpdateAPIView):
    permission_classes = [IsAuthenticated, isDoctor]
    queryset = Appointment.objects.all()
    serializer_class = ApproveApponmentByDoctor





class DoctorRegisterApi(viewsets.ViewSet):

    @action(detail=False, methods=['POST'], url_name='register')
    def doctor_register(self, request):
        serializer = DoctorRegistrationSerializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'success'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['POST'], url_path='login')
    def doctor_login(self, request):
        
        serializer = DoctorloginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']

            user = authenticate(username = phone_number, password=password)
            if user is not None:
                login(request, user)
                token = get_tokens_for_user(user)
                return Response({'message':'success', 'token':token}, status=status.HTTP_200_OK)
            else:
                return Response({'message':'invalid credentials'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        



