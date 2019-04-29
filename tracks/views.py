from django.shortcuts import render
from django.views import generic
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from .models import *
from rest_framework import viewsets
from .serializers import LastLocationSerializer, RouteSerializer, StepSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class StepViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Step.objects.all().order_by('timestamp')
    serializer_class = StepSerializer

class LastLocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = LastLocation.objects.all().order_by('timestamp')
    serializer_class = LastLocationSerializer


class RouteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Route.objects.all().order_by('init_time')
    serializer_class = RouteSerializer


def home(request):
	if request.method == 'GET':
		return render(request,"index.html");

def rutas(request):
	if request.method == 'GET':
		return render(request,"rutas.html");

'''@csrf_exempt
def last_locations_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        last_location = LastLocation.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = LastLocationSerializer(last_location)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LastLocationSerializer(last_location, data=data)
        print (serializer)
        print("HOLA")
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        last_location.delete()
        return HttpResponse(status=204)
        '''