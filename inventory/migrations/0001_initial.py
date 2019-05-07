# Generated by Django 2.0 on 2019-04-29 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import inventory.models
import inventory.utils.fields
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=100)),
                ('phoneNumber', phonenumber_field.modelfields.PhoneNumberField(default='', max_length=128, region=None, unique=True)),
                ('email', models.EmailField(default='', max_length=70, unique=True)),
                ('address', models.CharField(blank=True, default='', max_length=150)),
                ('profileImage', models.ImageField(blank=True, null=True, upload_to=inventory.models.get_image_path)),
                ('role', models.IntegerField(choices=[(0, 'Administrador'), (1, 'Cliente'), (2, 'Repartidor')], default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('token', models.CharField(default=None, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('latitudeGeo', models.FloatField(blank=True, default=0.0, null=True)),
                ('longitudeGeo', models.FloatField(blank=True, default=0.0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=inventory.models.getProdImagePath)),
                ('typeSelling', models.CharField(choices=[('unit', 'Unidad'), ('weight', 'Libra')], default='unit', max_length=20)),
                ('price', models.FloatField(blank=True, default=0.0, null=True)),
                ('isAvailable', models.BooleanField(default=True)),
                ('category', models.ForeignKey(default='General', on_delete=django.db.models.deletion.CASCADE, to='inventory.Category', to_field='name')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateCreated', models.DateTimeField(default=django.utils.timezone.now)),
                ('products', inventory.utils.fields.JSONField(default=dict)),
                ('totalPrice', models.FloatField(blank=True, default=0.0, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Solicitado'), (1, 'Armado'), (2, 'Por enviar'), (3, 'Entregado'), (-1, 'Cancelado')], default=0)),
                ('barCode', models.CharField(blank=True, default='{}', max_length=200, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=inventory.models.getOrderEvidenceImagePath)),
                ('deliveryCenter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.DeliveryCenter')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='userZone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='inventory.UserZone', to_field='name'),
        ),
    ]
