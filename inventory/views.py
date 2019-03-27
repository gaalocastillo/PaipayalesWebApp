from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Product
from .models import Category
from .models import User
from .forms import ProductForm

from rest_framework import generics
from rest_framework import permissions
from .serializers import ProductSerializer
from .serializers import UserSerializer
from .serializers import LoginSerializer
from rest_framework.response import Response
from rest_framework.views import status

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

    def post(self, request, *args, **kwargs):
        name = request.data.get("name", "")
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        address = request.data.get("address", "")
        if not name or not password or not email or not address:
            return Response(
                data={
                    "message": "name, address, email and password is required to register a user"
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
        new_user = User.objects.create(
            name=name, password=password, email=email, address=address
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )

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
        return Response(
            status=status.HTTP_200_OK
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


