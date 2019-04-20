from django.contrib.gis.db import models
from datetime import datetime
from django.conf import settings
from .utils import *

class LastLocation(models.Model):
    location = models.PointField()
    timestamp = models.DateTimeField(default=datetime.now)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)


class Step(models.Model):
    location = models.PointField() #default srid is 4326
    speed = models.DecimalField(default=0.000, max_digits=10, decimal_places=3)
    timestamp = models.DateTimeField(default=datetime.now)
    route = models.ForeignKey('Route', related_name='steps',on_delete=models.CASCADE)

    def __str__(self):
    	return str(self.location.x) + "," + str(self.location.y)
    
    class Meta:
    	ordering = ["timestamp"]
    	verbose_name = "Points of routes/Step"

class Route(models.Model):
    timestamp = models.DateTimeField(default=datetime.now)
    distance = models.DecimalField(default=0.000, max_digits=20, decimal_places=3)
    duration = models.DurationField(null=True)
    init_coord = models.PointField(null=True)
    end_coord = models.PointField(null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
    	return 'Route '+convert_date(self.timestamp) + ' of user '+self.user.name
    
    class Meta:
    	ordering = ["timestamp"]
    	verbose_name = "Route"