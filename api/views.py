from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer,UserProfileSerializer,ProductSerializer,AddressSerializer,CategorySerializer
from djoser.views import RegistrationView

@api_view(['GET'])
def api_root(request, fomart=None):
    """The api root"""
    return Response({
        
    })
class Registration(RegistrationView):
    def perform_create(self,serializer):
        user = serializer.save()
        customer = UserProfile(user=user)
        customer.save()
        super()
        
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileList(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
class ProductList(APIView):
    def get(self,request,format=None):
        pass
    def post(self,request,format=None):
        pass

class ProductDetail(APIView):
    def get_object(self,pk):
        pass
    def get(self,request,pk,format=None):
        pass
    def put(self,request,pk,format=None):
        pass
    def delete(self,request,pk,format=None):
        pass
# Create your views here.
