from django.shortcuts import render
import django_filters
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .models import UserProfile,Product,Category,Business,Sale
from .serializers import UserSerializer,UserProfileSerializer,ProductSerializer,CategorySerializer,BusinessSerializer,SalesSerializer
from djoser.views import RegistrationView

class ApiRootView(APIView):
    def get(self,request):
        return Response({
            'register': reverse('register', request=request),
            'obtain token': reverse('token-obtain',request=request),
            'users': reverse('user-list',request=request),
            'user profiles': reverse('user-profile-list',request=request),
            'categories': reverse('category-list', request=request),
            'products': reverse('product-list', request=request),
            'businesses': reverse('business-list', request=request),
            'sales': reverse('sales-list', request=request)
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

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('product_category','unit_price','shiping_price','shiped_on')
    
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BusinessList(generics.ListCreateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('name','county','owner','city','street')

class BusinessDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

class SalesList(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SalesSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('product','units','sold_at','business')

class SaleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SalesSerializer
# Create your views here.
