from rest_framework import serializers
from .models import Product
from .models import Category
from .models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "typeSelling", "price")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email")