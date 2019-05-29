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
from .models import DeliveryCenter
from .models import DELIVERY_MAN
from .models import CLIENT
from .models import ADMIN
from .forms import ProductForm
from .models import PURCHASE_STATE_CHOICES

from rest_framework import generics
from rest_framework import permissions
from .serializers import ProductSerializer
from .serializers import UserSerializer
from .serializers import UserZoneSerializer
from .serializers import LoginSerializer
from .serializers import DeliveryManListSerializer
from .serializers import PurchaseStateSerializer
from .serializers import PurchaseInfoSerializer
from .serializers import DeliveryCenterSerializer
from .serializers import PurchaseSerializer
from .serializers import MakePurchaseSerializer
from .serializers import ProcessPurchaseSerializer

from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from rest_framework.views import status
from .decorators import validate_request_data

from django.contrib.auth import authenticate
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
        role = request.data.get("role", "")
        file = request.data.get('file', "")
        if not name or not password or not email or not address or not userZone or not phoneNumber or not role:
            return Response(
                data={
                    "message": "name, address, userZone, email, phoneNumber, role and password is required to register a user"
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
        if int(role) not in {ADMIN, CLIENT, DELIVERY_MAN}:
            return Response(
                data={
                    "message": "The sent role does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        new_user = User.objects.create_user(email=email, password=password, phoneNumber=phoneNumber,
                    name=name)
        new_user.address = address
        new_user.userZone = userZoneObj
        new_user.profileImage = file
        new_user.role = int(role)
        token = create_token(new_user)
        new_user.token = str(token)
        new_user.save()
        data = {"access-token": new_user.token, 'role': int(new_user.role)}
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
        user = authenticate(username=email, password=password)
        if user is not None:
            data = {'access-token': str(user.token), 'role': int(user.role)}
            return HttpResponse(json.dumps(data, ensure_ascii=False).encode("utf-8"), content_type='application/json')
        else:
            return Response(
                data={
                    "message": "Invalid credentials."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

class ListUserZonesView(generics.ListCreateAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = UserZoneSerializer
    
    def get_queryset(self):
        queryset = UserZone.objects.order_by('name')[:]
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
    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            purchase = self.queryset.get(id=kwargs["pk"])
            serializer = PurchaseStateSerializer()
            updatedPurchase = serializer.update(purchase, request.data)
            return Response(PurchaseStateSerializer(updatedPurchase).data)
        except Purchase.DoesNotExist:
            return Response(
                data={
                    "message": "Purchase with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class PurchaseInfoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PurchaseInfoSerializer
    queryset = Purchase.objects.all()
    def get(self, request, *args, **kwargs):
        try:
            purchase = self.queryset.get(id=kwargs["pk"])
            return Response(PurchaseInfoSerializer(purchase).data)
        except Purchase.DoesNotExist:
            return Response(
                data={
                    "message": "Purchase with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class ListDeliveryCentersView(generics.ListCreateAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = DeliveryCenterSerializer
    
    def get_queryset(self):
        queryset = DeliveryCenter.objects.all()
        return queryset

class ListPurchasesView(generics.ListCreateAPIView):
    """
    Provides a get method handler for obtaining purchases that match with
    the status and delivery center given.
    """
    serializer_class = PurchaseSerializer
    
    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        idCenter = self.request.query_params.get('idCenter', None)
        queryset = None
        if status and idCenter:
            queryset = Purchase.objects.filter(status=status, deliveryCenter=idCenter)
        #Esto se ejecutara cuando se quiera obtener la lista de pedidos de un repartidor.
        #Para ello, hay que obtener el token de autenticacion del usuario de la cabecera.
        #elif status:
        #    queryset = Purchase.objects.filter(status=status)
        return queryset

class MakePurchaseView(generics.CreateAPIView):
    serializer_class = MakePurchaseSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        products = request.data.get("products", "")
        totalPrice = request.data.get("totalPrice", "")
        if not products:
            return Response(
                data={
                    "message": "Empty purchase. Please add at least one product."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        meta = request.META
        if('HTTP_AUTHORIZATION' not in meta or not User.objects.filter(token=meta['HTTP_AUTHORIZATION']).exists() or  
            int(User.objects.get(token=meta['HTTP_AUTHORIZATION']).role) != CLIENT):
            return Response(
                data={
                    "message": "Authorization denied. No valid authorization header found."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            user = User.objects.get(token=meta['HTTP_AUTHORIZATION'])
            purchase = Purchase.objects.create(products=products, totalPrice=totalPrice)
            purchase.user.add(user)
        return Response(
                data={
                    "message": "Purchase made."
                },
                status=status.HTTP_201_CREATED
            )

class ProcessPurchaseView(generics.CreateAPIView):
    serializer_class = ProcessPurchaseSerializer
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request, *args, **kwargs):
        id_ = request.data.get("id", "")
        userId = request.data.get("user", "")
        status_ = request.data.get("status", "")
        barCode = request.data.get("barCode", "")
        #photo = request.data['file']
        
        if not id_ or not userId or not status_ or not barCode:
            return Response(
                data={
                    "message": "Purchase id, delivery-man id, new status and barCode are needed to process the request."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if not Purchase.objects.filter(id=id_).exists():
            return Response(
                data={
                    "message": "Purchase not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if not User.objects.filter(id=userId).exists() or User.objects.get(id=userId).role != DELIVERY_MAN:
            return Response(
                data={
                    "message": "Delivery man not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if not isValidStatus(int(status_)):
            return Response(
                data={
                    "message": "Status not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        user = User.objects.get(id=int(userId))
        purchase = Purchase.objects.get(id=id_)
        users = purchase.user.all().values()
        for u in users:
            if u['role'] == DELIVERY_MAN:
                userObj = User.objects.get(id=u['id'])
                purchase.user.remove(userObj)
        purchase.user.add(user)
        purchase.barCode = barCode
        #purchase.photo = photo
        purchase.status = int(status_)
        purchase.save()
        return Response(
                data={
                    "message": "Purchase updated."
                },
                status = status.HTTP_200_OK
            )

class ListUserPurchasesView(generics.ListCreateAPIView):
    """
    Provides a get method handler for obtaining purchases that match with
    the status and delivery center given.
    """
    serializer_class = PurchaseSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        queryset = None
        meta = self.request.META
        if('HTTP_AUTHORIZATION' not in meta or not User.objects.filter(token=meta['HTTP_AUTHORIZATION']).exists() or  
            int(User.objects.get(token=meta['HTTP_AUTHORIZATION']).role) != CLIENT):
            return Response(
                data={
                    "message": "Authorization denied. No valid authorization header found."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            if status:
                user = User.objects.get(token=meta['HTTP_AUTHORIZATION'])
                queryset = Purchase.objects.filter(status=status, user=user)
        return queryset

def isValidStatus(status):
    for e in PURCHASE_STATE_CHOICES:
        if int(e[0]) == int(status):
            return True
    return False

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


