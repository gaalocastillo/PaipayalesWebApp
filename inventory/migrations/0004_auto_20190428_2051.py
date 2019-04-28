# Generated by Django 2.0 on 2019-04-28 20:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20190420_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('latitudeGeo', models.FloatField(blank=True, default=0.0, null=True)),
                ('longitudeGeo', models.FloatField(blank=True, default=0.0, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.UUIDField(default=uuid.UUID('6305d94b-8abf-44eb-9bd5-3852cb81c05c'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='purchase',
            name='deliveryCenter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.DeliveryCenter'),
        ),
    ]
