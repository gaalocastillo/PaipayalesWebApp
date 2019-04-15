from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from rest_framework_jwt.settings import api_settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Product
from .models import Category
from .models import UserZone
from .models import User
from .models import Purchase
from .models import DELIVERY_MAN
from .forms import ProductForm

from rest_framework import generics
from rest_framework import permissions
from .serializers import ProductSerializer
from .serializers import UserSerializer
from .serializers import UserZoneSerializer
from .serializers import LoginSerializer
from .serializers import DeliveryManListSerializer
from .serializers import PurchaseStateSerializer

from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from rest_framework.views import status

from .utils.tokenization import jwt_payload_handler
from .utils.tokenization import create_token
import json
import uuid

class ListProductsView(generics.ListCreateAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        cat = self.kwargs['cat'].strip().capitalize()
        queryset = Product.objects.filter(category=cat)
        return queryset

class RegisterUsers(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request, *args, **kwargs):
        name = request.data.get("name", "")
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        phoneNumber = request.data.get("phoneNumber", "")
        address = request.data.get("address", "")
        userZone = request.data.get("userZone", "")
        file = request.data['file']
        if not name or not password or not email or not address or not userZone or not phoneNumber:
            return Response(
                data={
                    "message": "name, address, userZone, email, phoneNumber and password is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if not isValidEmail(email):
            return Response(
                data={
                    "message": "The email entered already has an account associated."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            userZoneObj = UserZone.objects.get(name=userZone)
        except UserZone.DoesNotExist:
            return Response(
                data={
                    "message": "The sent userZone does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        id_ = uuid.uuid4()
        new_user = User.objects.create(
            id=id_, name=name, password=password, email=email, address=address, userZone=userZoneObj, 
                phoneNumber=phoneNumber, profileImage=file, token=None)
        token = create_token(new_user)
        new_user.token = str(token)
        new_user.save()
        data = {"access-token": new_user.token}
        return HttpResponse(json.dumps(data, ensure_ascii=False).encode("utf-8"), content_type='application/json')

class LoginUser(generics.CreateAPIView):
    """
    POST auth/login/
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        if not password or not email:
            return Response(
                data={
                    "message": "email and password are required to login a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if not isValidLogin(email=email, password=password):
            return Response(
                data={
                    "message": "Invalid credentials."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        user = User.objects.get(email=email, password=password)
        data = {'access-token': str(user.token)}
        return HttpResponse(json.dumps(data, ensure_ascii=False).encode("utf-8"), content_type='application/json')

class ListUserZonesView(generics.ListCreateAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = UserZoneSerializer
    
    def get_queryset(self):
        queryset = UserZone.objects.all()
        return queryset


class ListDeliveryManView(generics.ListCreateAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = DeliveryManListSerializer
    
    def get_queryset(self):
        queryset = User.objects.filter(role=DELIVERY_MAN)
        return queryset

class PurchaseStateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PurchaseStateSerializer
    queryset = Purchase.objects.all()
    def get(self, request, *args, **kwargs):
        try:
            purchase = self.queryset.get(id=kwargs["pk"])
            return Response(PurchaseStateSerializer(purchase).data)
        except Purchase.DoesNotExist:
            return Response(
                data={
                    "message": "Purchase with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

def isValidEmail(email):
    """
    Method used for identifying duplicated emails when registering
    a new user account.
    """
    return not User.objects.filter(email=email).exists()

def isValidLogin(email, password):
    """
    Method used for validating a user crendentials.
    """
    return User.objects.filter(email=email, password=password).exists()

def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'inventory/index.html', context)


def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'inventory/detail.html', {'product': product})


def addnew(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        print(dir(form))
        if form.is_valid():
            # product = form.save(commit=True)
            form.save()

            # product = Product()
            # product.name = form.cleaned_data['name']
            # product.cetagory = form.cleaned_data['cetagory']
            # product.supplier = form.cleaned_data['supplier']
            # product.unit_price = form.cleaned_data['unit_price']
            # product.description = form.cleaned_data['description']
            # product.save()
            # return redirect('detail', pk=product.pk)
            return redirect('index')
    else:
        form = ProductForm()
    return render(request, 'inventory/new.html', {'form': form})


def edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/edit.html', {'form': form})


