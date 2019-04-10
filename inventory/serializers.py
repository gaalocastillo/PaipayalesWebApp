from rest_framework import serializers
from .models import Product
from .models import Category
from .models import User
from .models import UserZone

class ProductSerializer(serializers.ModelSerializer):
# https://stackoverflow.com/questions/32219130/django-rest-framework-imagefield-to-server?rq=1

    class Meta:
        model = Product
        fields = ("name", "typeSelling", "price", "photo")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "phoneNumber", "profileImage", "password", "address", "userZone")

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")

class UserZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserZone
        fields = ("name",)