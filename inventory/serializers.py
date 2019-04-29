from rest_framework import serializers
from .models import Product
from .models import Category
from .models import User
from .models import UserZone
from .models import Purchase
from .models import DeliveryCenter

class ProductSerializer(serializers.ModelSerializer):
# https://stackoverflow.com/questions/32219130/django-rest-framework-imagefield-to-server?rq=1

    class Meta:
        model = Product
        fields = ("id", "name", "typeSelling", "price", "photo")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "phoneNumber", "profileImage", "password", "address", "userZone", "role")

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")

class UserZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserZone
        fields = ("name",)

class DeliveryManListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name",)

class PurchaseStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ("id", "status",)

class PurchaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ("id", "products",)

class DeliveryCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCenter
        fields = ("id", "name", "latitudeGeo", "longitudeGeo")

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ("id", "dateCreated", "barCode", "status", "products",)

class MakePurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ("products")