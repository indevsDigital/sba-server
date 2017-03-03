from django.shortcuts import render,get_object_or_404
import django_filters
from django.db.models import Sum
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .models import UserProfile,Product,Category,Business,Receipt
from .serializers import UserSerializer,UserProfileSerializer,ProductSerializer,\
                    CategorySerializer,BusinessSerializer,ReceiptSerializer,\
                    SellerSerializer,DamagedItemsSerializer,ItemsBoughtSerializer,ProductSimpleSerializer
from djoser.views import RegistrationView
from django.utils.six import BytesIO
from django.utils import timezone
from rest_framework.parsers import JSONParser
from rest_framework import status
from .random_string import generate_a_receipt_number
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
            'receipts': reverse('receipts-list', request=request),
            'sell': reverse('sell', request=request)
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
class SimpleProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSimpleSerializer
    
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('product_category','unit_price','shiping_price','purchase_date')



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

class ReceiptsList(generics.ListCreateAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('product','units','sold_at','business')

class ReceiptDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

class SellItem(APIView):
    """sell items in stock"""
    def post(self,request):
        data = JSONParser().parse(request)
        serializer = SellerSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            product = get_object_or_404(Product,pk=data.product_id,business__id=data.business_id)
            if product.available_units < data.number_of_units:
                return Response('Number of items remaining are not enough',status=status.HTTP_400_BAD_REQUEST)
            else:
               product.available_units -= data.number_of_units
               product.sold_unit += data.number_of_units
               total = product.unit_price * data.number_of_units
               product.save()
               newproduct = get_object_or_404(Product,pk=data.product_id,business__id=data.business_id)
               business = get_object_or_404(Business,pk=data.business_id)
               receipt_no = generate_a_receipt_number(business.name,total)
               receipt = Receipt.objects.create(product=newproduct,units=data.number_of_units,sold_at=timezone.now(),business=business,receipt_number=receipt_no,total_amount=total)
               return Response(ReceiptSerializer(receipt,context={'request':request}).data,status=status.HTTP_200_OK)
        return Response('data  is not valid',status=status.HTTP_400_BAD_REQUEST)

class DamagedItems(APIView):
    """list items damaged in stock"""
    def post(self,request):
        data = JSONParser().parse(request)
        serializer = DamagedItemsSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            product = get_object_or_404(Product,pk=data.product_id)
            product.damaged_units += data.units
            product.available_units -= data.units
            product.save()
            return Response('%d units have been recorded damaged'%data.units,status=status.HTTP_200_OK)
        return Response('data is not valid',status=status.HTTP_400_BAD_REQUEST)    
