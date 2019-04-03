from rest_framework import serializers
from .models import Product
from .models import Category
from .models import User
from .models import UserZone

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "typeSelling", "price")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "password", "address", "userZone")

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")

class UserZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserZone
        fields = ("name",)