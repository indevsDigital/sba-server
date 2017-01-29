from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
# Create your views here.
