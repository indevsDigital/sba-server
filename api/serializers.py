from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
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
    pass

class CategorySerializer(serializers.ModelSerializer):
    pass

class AddressSerializer(serializers.ModelSerializer):
    pass