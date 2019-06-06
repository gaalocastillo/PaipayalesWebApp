"""tracker_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.gis import admin
#from django.contrib import admin
from tracks import views
from rest_framework import routers, serializers, viewsets
#from django.urls import include, path
from rest_framework import routers
from tracks import views
from rest_framework.schemas import get_schema_view
from django.urls import path

#schema_view = get_schema_view(title='Pastebin API')

router = routers.DefaultRouter()
router.register(r'lastlocations', views.LastLocationViewSet)
#router.register(r'steps', views.StepsList.as_view())
#router.register(r'routes', views.RouteViewSet)


urlpatterns = [
    url(r'^$', views.home, name='last_locations'),
    url(r'^rutas/', views.rutas, name='rutas'),
    url(r'^api/v1/steps/(?P<pk>\d+)$', views.StepDetail.as_view()),
    url(r'^api/v1/steps', views.StepsList.as_view()),
    url(r'^api/v1/purchasesxworker$', views.pedidos_por_repartidor),
    url(r'^api/v1/latestroute-dm/(?P<id_dm>\d+)$', views.last_route_deliveryman),
    url(r'^api/v1/routes/(?P<pk>\d+)$', views.RouteDetail.as_view()),
    url(r'^api/v1/routes', views.RoutesList.as_view()),

    url(r'^api/v1/', include(router.urls), name='api'),
    url(r'^api-auth/', include('rest_framework.urls')),
    #url(r'^schema/', schema_view),
    #url(r'^api/v1/lastlocations/(?P<pk>\d+)/', views.last_locations_detail),

]