from django.shortcuts import render,get_object_or_404
import django_filters
from django.db.models import Sum,F,FloatField
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
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from django_filters import rest_framework as filters
class ApiRootView(APIView):
    """The root of the api describe all the urls for the resources"""
    permission_classes = (IsAuthenticated,)
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
            'sell': reverse('sell', request=request),
            'simple product list': reverse('simple-product-list', request=request),
            'damaged units': reverse('damaged', request=request),
            'bought units account': reverse('bought', request=request),            
            'damaged units account': reverse('damaged-account', request=request),
            'sold units account': reverse('sold-account', request=request),
            'remaining units account': reverse('remaining-account', request=request),                                    
             })

class Registration(RegistrationView):
    def perform_create(self,serializer):
        user = serializer.save()
        customer = UserProfile(user=user)
        customer.save()
        super()

class UserList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileList(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
class SimpleProductList(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Product.objects.all()
    serializer_class = ProductSimpleSerializer
    
class ProductList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('product_category','unit_price','shiping_price','purchase_date')



class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BusinessList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('name','county','owner','city','street')

class BusinessDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

class ReceiptsList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('product','units','sold_at','business')

class ReceiptDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

class SellItem(APIView):
    permission_classes =(IsAuthenticated,)
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
    permission_classes = (IsAuthenticated,)
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

class AccountItemsBoughtFilter(filters.FilterSet):
    date_range = django_filters.DateFromToRangeFilter(name='purchase_date')
    unit_price_range = django_filters.NumericRangeFilter(name='unit_price')
    class Meta:
        model = Product
        fields = ['product_category','unit_price','purchase_date','unit_price_range']

class AccountItemsBought(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSimpleSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = AccountItemsBoughtFilter

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        total = queryset.aggregate(sum=Sum('unit_price'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'data':serializer.data,'total sum of bought units':total})
        seriaizer = ProductSimpleSerializer(queryset,many=True)
        return Response({'data': seriaizer.data,'total_price':total})

class DamagedItemsAccount(generics.ListAPIView):
    queryset=Product.objects.filter(damaged_units__gte=1)
    serializer_class = ProductSimpleSerializer

    def list(self,request):
        queryset = self.get_queryset()
        total = queryset.aggregate(sum=Sum(F('damaged_units')*F('unit_price'), output_field=FloatField()))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'data':serializer.data,'total sum of damaged units':total})
        serializer = ProductSimpleSerializer(queryset,many=True)
        return Response({'data':serializer.data,'total_damaged_units':total})

class SoldItemsAccount(generics.ListAPIView):
    queryset = Product.objects.filter(sold_unit__gte=1)
    serializer_class = ProductSimpleSerializer

    def list(self,request):
        queryset = self.get_queryset()
        total = queryset.aggregate(sum=Sum(F('sold_unit')*F('unit_price'), output_field=FloatField()))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'data':serializer.data,'total sum of sold units':total})

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data':serializer.data,'total sum of sold items':total})

class RemainingItemsAccount(generics.ListAPIView):
    queryset = Product.objects.filter(available_units__gte=1)
    serializer_class = ProductSimpleSerializer

    def list(self,request):
        queryset = self.get_queryset()
        total = queryset.aggregate(sum=Sum(F('available_units')*F('unit_price'), output_field=FloatField()))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'data':serializer.data,'total sum of remaining units':total})

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data':serializer.data,'total sum of remaining items':total})