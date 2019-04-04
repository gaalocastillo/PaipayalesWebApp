from django.db import models
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

TYPE_SELLING_CHOICES = (
    ("unit", "UNIT"),
    ("weight", "WEIGHT")
)

class UserZone(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    phoneNumber = PhoneNumberField(null=False, blank=False, unique=True, default="")
    email = models.EmailField(max_length=70,blank=True, unique=True)
    password = models.CharField(max_length=15)
    address = models.CharField(max_length=150, blank=True, null=False)
    userZone = models.ForeignKey(UserZone, to_field="name", on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return 'Id:{0} Name:{1}'.format(self.id, self.name)

class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=True, null=True, default="")
    #photo =
    typeSelling = models.CharField(max_length=20, choices=TYPE_SELLING_CHOICES, default='unit')
    price = models.FloatField(null=True, blank=True, default=0.0)
    category = models.ForeignKey(Category, to_field="name" ,on_delete=models.CASCADE, null=False, default="General", blank=False)
    isAvailable = models.BooleanField(default=True)

    def __str__(self):
        return 'Id:{0} Name:{1}'.format(self.id, self.name) 

class Purchase(models.Model):
    dateCreated = models.DateTimeField(default=timezone.now)
#    order = JSONField()            This field will be included when start using postgresql
    totalPrice = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return self.id
