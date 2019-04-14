from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import django.contrib.gis.admin as geoAdmin
from .models import *

admin.site.register(Step, geoAdmin.OSMGeoAdmin)
admin.site.register(Route, geoAdmin.OSMGeoAdmin)
admin.site.register(LastLocation, geoAdmin.OSMGeoAdmin)


