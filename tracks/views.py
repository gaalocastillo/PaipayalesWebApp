from django.shortcuts import render
from django.views import generic
from tracks.models import *
from inventory.models import *
from rest_framework import viewsets
from tracks.serializers import *
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point

'''
class StepViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Step.objects.all().order_by('timestamp')
    serializer_class = StepSerializer
'''
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

def pedidos_por_repartidor(request,token):
    '''
    End-point que enlista todos los pedidos relacionados a un repartidor.
    Params: token del repartidor
    Respuesta: lista de pedidos, dentro de un diccionario
    '''
    if request.method == 'GET':
        #obtener usuario de acuerdo al token
        #user = obtener_usuario(token)
        user = User.objects.get(pk=token)
        if (user != None):
            purchases = user.purchase_set.all().values('id', 'dateCreated')
            response = {}
            response["purchases"] = purchases
            return JsonResponse(response)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
        

class StepsList(APIView):
    """
    Lista todas las coordenadas de todas las rutas, o crea un par de coordenadas asociadas a una ruta.
    """
    def get(self, request, format=None):
        steps = Step.objects.all()
        serializer = StepSerializer(steps, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        if(not "latitude" in data or not "longitude" in data):
            return Response( status=status.HTTP_400_BAD_REQUEST)

        data["location"] = Point(float(data["latitude"]),float(data["longitude"]))
        del data["latitude"]
        del data["longitude"]
        serializer = StepSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            response={}
            response["id"] = serializer.data["id"]
            return JsonResponse(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StepDetail(APIView):
    """
    End-points para btener, actualizar o eliminar un objeto tipo Step.
    """
    def get_object(self, pk):
        try:
            return Step.objects.get(pk=pk)
        except Step.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        step = self.get_object(pk)
        serializer = StepSerializer(step)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        step = self.get_object(pk)
        serializer = StepSerializer(step, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        step = self.get_object(pk)
        step.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoutesList(APIView):
    """
    Lista todas las rutas o crea una.
    """
    def get(self, request, format=None):
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RouteSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response={}
            response["id"] = serializer.data["id"]
            return JsonResponse(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RouteDetail(APIView):
    """
    End-points para obtener, actualizar o eliminar una instancia de una ruta.
    """
    def get_object(self, pk):
        try:
            return Route.objects.get(pk=pk)
        except Route.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        route = self.get_object(pk)
        serializer = RouteSerializer(route)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        route = self.get_object(pk)
        serializer = RouteSerializer(route, data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        route = self.get_object(pk)
        route.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#def obtener_usuario(token):
