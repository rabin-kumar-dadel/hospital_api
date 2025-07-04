from accounts.forms import *
from accounts.mixins import *
from rest_framework.response import Response
from rest_framework import status
from accounts.doctor_apis.serializer import *
from rest_framework.response import Response
from accounts.api.serializer import *
from rest_framework.mixins import *
from rest_framework.generics import *
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.permission import *
from rest_framework.views import APIView
from accounts.authorize_apis.serializer import *


# for the token authentication 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }





# authorized user registration view
class AuthorizedRegisterAPIView(APIView):
    def post(self, request):
        serializer = AuthorizedRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response({
            "message": "Registration successful",
            "role": request.data.get("role"),
            "phone_number":request.data.get("phone_number")
        }, status=status.HTTP_201_CREATED)

# authorize user login view
class AuthorizedLoginAPIView(APIView):
    def post(self, request):
        serializer = AuthorizedLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            "message": "Login successful",
            "data": serializer.validated_data
        }, status=status.HTTP_200_OK)


