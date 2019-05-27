from django.contrib.gis.db import models
from datetime import datetime
from django.conf import settings
from .utils import *
from inventory.models import Purchase

class LastLocation(models.Model):
    location = models.PointField()
    timestamp = models.DateTimeField(default=datetime.now)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)


class Step(models.Model):
    """
    Modelo de un par de coordenadas. Una instancia de este modelo representa
    a un par de coordenadas, que son parte de una ruta seguida por un repartidor.
    location: latitud,longitud
    timestamp: fecha y hora en las que fue tomada este par de coordenadas.
    route: ruta a la cual pertenece el par de coordenadas
    """
    location = models.PointField() #default srid is 4326
    #speed = models.DecimalField(default=0.000, max_digits=10, decimal_places=3)
    timestamp = models.DateTimeField(default=datetime.now)
    route = models.ForeignKey('Route', related_name='steps',on_delete=models.CASCADE)

    def __str__(self):
    	return str(self.location.x) + "," + str(self.location.y)
    
    class Meta:
    	ordering = ["timestamp"]
    	verbose_name = "Points of routes/Step"

class Route(models.Model):
    """
    Modelo de las rutas.
    """
    init_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)
    distance = models.DecimalField(default=0.000, max_digits=20, decimal_places=3)
    #duration = models.DurationField(null=True, blank=True)
    origin = models.PointField(null=True)
    destination = models.PointField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE, null=True)

    def __str__(self):
    	return 'Route '+convert_date(self.init_time) + ' of user '+str(self.user.id)
    
    class Meta:
    	ordering = ["init_time"]
    	verbose_name = "Route"