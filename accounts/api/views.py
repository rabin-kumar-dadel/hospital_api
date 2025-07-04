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


# patient register view
class PatientRegisterApiView(CreateAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = "User created successfully!"
        return response


# patient login view
class PatientLoginView(GenericAPIView):
    serializer_class = PatientLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # ✅ Add custom message to response
        return Response({
            "message": "patient logged in successfully.",
            "refresh": data['refresh'],
            "access": data['access'],
        }, status=status.HTTP_200_OK)



# Patient appoinment creating veiw
class AppointmentPatientCreate(viewsets.ModelViewSet):
    serializer_class = ApponmentSerializer
    permission_classes = [IsAuthenticated, ispatient]
    queryset = Appointment.objects.all()
    throttle_classes = [UserRateThrottle]


    def perform_create(self, serializer):
        serializer.save(patient = self.request.user)
        


