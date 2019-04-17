from django.db import models
from django.conf import settings

from django.utils import timezone
import os
import uuid

from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import BaseUserManager

TYPE_SELLING_CHOICES = (
    ("unit", "Unidad"),
    ("weight", "Libra")
)

REQUESTED = 0
PACKED = 1
TO_BE_SENT = 2
DELIVERED = 3
CANCELLED = -1

PURCHASE_STATE_CHOICES = (
    (REQUESTED, "Solicitado"),
    (PACKED, "Armado"),
    (TO_BE_SENT, "Por enviar"),
    (DELIVERED, "Entregado"),
    (CANCELLED, "Cancelado"),
)

ADMIN = 0
CLIENT = 1
DELIVERY_MAN = 2

USER_ROLE_CHOICES = (
    (ADMIN, "Administrador"),
    (CLIENT, "Cliente"),
    (DELIVERY_MAN, "Repartidor"),
)

PRODUCTS_IMAGES_DIR = 'images/products_pics' 
PROFILE_IMAGES_DIR = 'images/profile_pics'
ORDER_EVIDENCES_DIR = 'images/orders_evidence_pics'
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.user')

def get_image_path(instance, filename):
    return '/'.join([PROFILE_IMAGES_DIR, str(instance.id), filename])

def getProdImagePath(instance, filename):
    return '/'.join([PRODUCTS_IMAGES_DIR, str(instance.id), filename])

def getOrderEvidenceImagePath(instance, filename):
    return '/'.join([ORDER_EVIDENCES_DIR, str(instance.id), filename])

class UserZone(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name

class User(models.Model):
    REQUIRED_FIELDS = ('user',)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    phoneNumber = PhoneNumberField(null=False, blank=False, unique=True, default="")
    email = models.EmailField(max_length=70,blank=True, unique=True)
    password = models.CharField(max_length=15)
    address = models.CharField(max_length=150, blank=True, null=False)
    profileImage = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    userZone = models.ForeignKey(UserZone, to_field="name", on_delete=models.PROTECT, null=True, blank=True)
    role = models.IntegerField(default=CLIENT, choices=USER_ROLE_CHOICES)

    token = models.CharField(max_length=200, default=None, null=True)
    USERNAME_FIELD = 'email'
    is_authenticated = False
    objects = models.Manager()

    def __str__(self):
        return 'Id:{0} Name:{1}'.format(self.id, self.name)

class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=True, null=True, default="")
    photo = models.ImageField(upload_to=getProdImagePath, blank=True, null=True)
    typeSelling = models.CharField(max_length=20, choices=TYPE_SELLING_CHOICES, default='unit')
    price = models.FloatField(null=True, blank=True, default=0.0)
    category = models.ForeignKey(Category, to_field="name" ,on_delete=models.CASCADE, null=False, default="General", blank=False)
    isAvailable = models.BooleanField(default=True)

    def __str__(self):
        return 'Id:{0} Name:{1}'.format(self.id, self.name) 

class DeliveryCenter(models.Model):
    name = models.CharField(max_length=200)
    latitudeGeo = models.FloatField(null=True, blank=True, default=0.0)
    longitudeGeo = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return str(self.id)

class Purchase(models.Model):
    dateCreated = models.DateTimeField(default=timezone.now)
    products = models.CharField(max_length=200, blank=False, null=False, default='{}')
#    order = JSONField()            This field will be included when start using postgresql
    totalPrice = models.FloatField(null=True, blank=True, default=0.0)
    status = models.IntegerField(default=REQUESTED, choices=PURCHASE_STATE_CHOICES)
    barCode = models.CharField(max_length=200, blank=True, null=True, default='{}')
    photo = models.ImageField(upload_to=getOrderEvidenceImagePath, blank=True, null=True)
    user = models.ManyToManyField(User)
    deliveryCenter = models.ForeignKey(DeliveryCenter, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.id)
