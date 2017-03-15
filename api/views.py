from django.shortcuts import render,get_object_or_404
import django_filters
from django.db.models import Sum,F,FloatField
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .models import UserProfile,Product,Category,Business,Receipt,ReceiptItems
from .serializers import UserSerializer,UserProfileSerializer,ProductSerializer,\
                    CategorySerializer,BusinessSerializer,ReceiptSerializer,\
                    SellerSerializer,DamagedItemsSerializer,ItemsBoughtSerializer,ProductSimpleSerializer,ReceiptItemsSerializer
from djoser.views import RegistrationView
from django.utils.six import BytesIO
from django.utils import timezone
from rest_framework.parsers import JSONParser
from rest_framework import status
from .random_string import generate_a_receipt_number
from rest_framework.permissions import IsAdminUser
from django_filters import rest_framework as filters
from django.db import transaction
from rest_framework.exceptions import ValidationError
class ApiRootView(APIView):
    """The root of the api describe all the urls for the resources"""
    def get(self,request):
        return Response({
            'register': reverse('register', request=request),
            'obtain token': reverse('token-obtain',request=request),
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
            'Profits and Losses account': reverse('profit-losses-account', request=request),
            'User details for logged in user': reverse('details', request=request)                         
                                          
             })

class Registration(RegistrationView):
    def perform_create(self,serializer):
        user = serializer.save()
        customer = UserProfile(user=user)
        customer.save()
        super()
class UserDetails(APIView):
    def get(self,request):
        user = get_object_or_404(User,username=request.user)
        profile = user.userprofile
        business = user.userprofile.business
        user_data = UserSerializer(user).data
        profile_data = UserProfileSerializer(profile,context={'request': request}).data
        business_data = BusinessSerializer(business,context={'request': request}).data
        return Response({
            'User': user_data,
            'profile': profile_data,
            'business': business_data
        })
class SimpleProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSimpleSerializer

    def list(self,request):
        user = request.user
        queryset = Product.objects.filter(business=user.userprofile.business)
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)
    
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('product_category','unit_price','purchase_date')



class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self,request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer(queryset,many=True)
        return Response(serializer_class.data)
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
    filter_fields = ('sold_at','business')

class ReceiptDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

class SellItem(APIView):
    """sell items in stock"""
    @transaction.atomic
    def post(self,request):
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            total_selling_price = 0
            total_buying_price = 0           
            business = get_object_or_404(Business,pk=data.business_id)
            receipt_no = generate_a_receipt_number(business.name,total_selling_price)
            receipt = Receipt.objects.create(business=business,receipt_number=receipt_no,served_by=request.user)            
            for data in data.product:
                product = get_object_or_404(Product,pk=int(data['pk']))
                if product.available_units < int(data['number_of_units']):
                    raise ValidationError('Requested units are not enough for  ' + str(product.product_name))
                else:
                    product.available_units -= int(data['number_of_units'])
                    product.sold_unit += int(data['number_of_units'])
                    total_selling_price += (int(data['selling_price']) * int(data['number_of_units']))
                    total_buying_price += product.unit_price * int(data['number_of_units'])
                    items_return = total_selling_price - total_buying_price
                    product.save()
                    newproduct = get_object_or_404(Product,pk=int(data['pk']))
                    ReceiptItems.objects.create(receipt=receipt,product=newproduct,selling_price_per_unit=int(data['selling_price']),
                                            units=int(data['number_of_units']),items_return=items_return)
            receipt.total_selling_price = total_selling_price
            receipt.save()   
            return Response(ReceiptSerializer(receipt,context={'request':request}).data,status=status.HTTP_200_OK)
        return Response('data  is not valid',status=status.HTTP_400_BAD_REQUEST)
class DamagedItems(APIView):
    """list items damaged in stock"""
    def post(self,request):
        serializer = DamagedItemsSerializer(data=request.data)
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
        total = queryset.aggregate(sum=Sum(F('unit_price')*F('total_inital_units'), output_field=FloatField()))
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

class ProfitsLossesAccounts(generics.ListAPIView):
    queryset = ReceiptItems.objects.all()
    serializer_class = ReceiptItemsSerializer

    def list(self,request):
        queryset = self.get_queryset()
        total = queryset.aggregate(sum=Sum('items_return'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'data':serializer.data,'total sum returns':total})

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data':serializer.data,'total sum returns':total})
