from django import forms
from .models import Product

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'price', 'description', 'typeSelling', 'category', 'photo', 'isAvailable')
        labels = {
            "name": "Nombre",
            'price': 'Precio',
            'description': 'Descripción',
            'typeSelling': 'Tipo de venta',
            'category': 'Categoría',
            'photo': 'Foto',
            'isAvailable': 'Disponible'
        }
