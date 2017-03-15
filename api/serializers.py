from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile,Product,Category,Business,Receipt,ReceiptItems
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','email','first_name','last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Creates a new User
        """
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """Updates and returns a new `User` Instance"""
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True,view_name="user-detail")
    class Meta:
        model = UserProfile
        fields = ('id','user','phone_number','avatar','national_id')

    def create(self, validated_data):
        """
        Creates a new User
        """
        return UserProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Updates and returns a new `User` Instance"""
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.avatar = validated_data.get(
            'avatar', instance.avatar)
        instance.national_id = validated_data.get(
            'national_id', instance.national_id)
        instance.save()
        return instance
class ProductSerializer(serializers.ModelSerializer):
    product_category = serializers.HyperlinkedRelatedField(queryset=Category.objects.all(),view_name="category-detail")
    business = serializers.HyperlinkedRelatedField(queryset=Business.objects.all(),view_name='business-detail')
    
    class Meta:
        model = Product
        fields = ('id','product_name','product_code','description','product_category','unit_price','purchase_date','total_inital_units','business','end_on','expires_on','available_units','sold_unit','damaged_units')
        
    def create(self,validated_data):
        return Product.objects.create(**validated_data)

    def update(self,instance,validated_data):
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.product_code = validated_data.get('product_code', instance.product_code)
        instance.product_category = validated_data.get('product_category', instance.product_category)
        instance.unit_price = validated_data.get('unit_price', instance.unit_price)
        instance.purchase_date = validated_data.get('purchase_date', instance.purchase_date)
        instance.total_inital_units = validated_data.get('total_inital_units', instance.total_inital_units)
        instance.business = validated_data.get('business', instance.business)
        instance.product_name = validated_data.get('product_name', instance.product_name)        
        instance.end_on = validated_data.get('end_on', instance.end_on)
        instance.expires_on = validated_data.get('expires_on', instance.expires_on)
        instance.description = validated_data.get('description', instance.description)                                                        
        instance.save()
        return instance
class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','product_name','product_code','available_units','unit_price')
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    business = serializers.HyperlinkedRelatedField(queryset=Business.objects.all(),view_name='business-detail')    
    class Meta:
        model = Category
        fields = ('id','name','business')

    def create(self,validated_data):
        return Category.objects.create(**validated_data)

    def update(self,instance,validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance



class BusinessSerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedRelatedField(queryset=UserProfile.objects.all(),view_name='details')
    class Meta:
        model = Business
        fields = ('id','name','county','owner','city','street')
    def create(self,validated_data):
        return Business.objects.create(**validated_data)

    def update(self,instance,validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.county = validated_data.get('county', instance.county)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.city = validated_data.get('city', instance.city)
        instance.street = validated_data.get('street', instance.street)
        instance.save()
        return instance
        
class ReceiptSerializer(serializers.ModelSerializer):
    business = serializers.HyperlinkedRelatedField(queryset=Business.objects.all(),view_name='business-detail')
    served_by = serializers.HyperlinkedRelatedField(queryset=User.objects.all(),view_name='user-profile')
    class Meta:
        model = Receipt
        fields = ('id','sold_at','business','receipt_number','total_selling_price','served_by')

    def create(self,validated_data):
        return Receipt.objects.all()
class ReceiptItemsSerializer(serializers.ModelSerializer):
    receipt = serializers.HyperlinkedRelatedField(queryset=Receipt.objects.all(),view_name='receipt-detail')
    product = serializers.HyperlinkedRelatedField(queryset=Product.objects.all(),view_name='product-detail')
    
    class Meta:
        model = ReceiptItems
        fields = ('receipt','product','selling_price_per_unit','units','items_return')
        
class Seller(object):
    def __init__(self,business_id,product):
        self.business_id = business_id
        self.product = product
        
class DocumentListField(serializers.DictField):
    child = serializers.CharField()

class StringListField(serializers.ListField):
    child = DocumentListField()

class SellerSerializer(serializers.Serializer):
    business_id = serializers.IntegerField()
    product = StringListField()

    def create(self,validated_data):
        return Seller(**validated_data)

class DamagedItems(object):
    def __init__(self,units,product_id):
        self.units = units
        self.product_id = product_id

class DamagedItemsSerializer(serializers.Serializer):


    units = serializers.IntegerField()
    product_id = serializers.IntegerField()

    def create(self,validated_data):
        return DamagedItems(**validated_data)

class ItemsBoughtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','product_name','unit_price')