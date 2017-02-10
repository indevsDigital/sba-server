from django.shortcuts import render
import django_filters
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .models import UserProfile,Product,Category
from .serializers import UserSerializer,UserProfileSerializer,ProductSerializer,AddressSerializer,CategorySerializer
from djoser.views import RegistrationView

class ApiRootView(APIView):
    def get(self,request):
        return Response({'users': reverse('user-list',request=request) })

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

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('product_category','unit_price','shiping_price','shiped_on')
    

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
# Create your views here.
