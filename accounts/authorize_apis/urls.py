
from django.urls import path,include
from accounts.doctor_apis.views import *
from rest_framework.routers import DefaultRouter
from accounts.authorize_apis.views import *

urlpatterns = [
   
    path('api/register/', AuthorizedRegisterAPIView.as_view(), name='authorize_registration'),
    path('api/login/', AuthorizedLoginAPIView.as_view(), name='authorize_login'),

]


