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
from rest_framework.decorators import api_view
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

ADMIN = 0
CLIENT = 1
DELIVERY_MAN = 2

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

@api_view(['GET' ])
def pedidos_por_repartidor(request):
    '''
    End-point que enlista todos los pedidos relacionados a un repartidor.
    Params: token del repartidor
    Respuesta: lista de pedidos, dentro de un diccionario con clave data
    {"data":[]}
    '''
    if request.method == 'GET':
        meta = request.META
        print(meta['HTTP_AUTHORIZATION'])
        if('HTTP_AUTHORIZATION' not in meta or not User.objects.filter(token=meta['HTTP_AUTHORIZATION']).exists() or  
            int(User.objects.get(token=meta['HTTP_AUTHORIZATION']).role) != DELIVERY_MAN):
            return Response(
                data={
                    "message": "Authorization denied. No valid authorization header found."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        #obtener usuario de acuerdo al token
        user = User.objects.get(token=meta['HTTP_AUTHORIZATION'])

        purchases = user.deliveries.filter(status=PACKED).values('id', 'user__address')
        purchases = list(purchases)
        
        response = {}
        response["data"] = purchases
        return JsonResponse(response)
    else:
        return Response(data={
                    "message": "Bad request."
                },status=status.HTTP_400_BAD_REQUEST)
        

class StepsList(APIView):
    """
    Lista todas las coordenadas de todas las rutas, o crea un par de coordenadas asociadas a una ruta.
    Para crear un Step se debe seguir el formato:
    {"latitude":0,"longitude":0,"route":1}
    """
    def get(self, request, format=None):
        steps = Step.objects.all()
        serializer = StepSerializer(steps, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        #se verifica primero que se haya adjuntado el token como header
        meta = request.META
        if('HTTP_AUTHORIZATION' not in meta or not User.objects.filter(token=meta['HTTP_AUTHORIZATION']).exists() or  
            int(User.objects.get(token=meta['HTTP_AUTHORIZATION']).role) != DELIVERY_MAN):
            return Response(
                data={
                    "message": "Authorization denied. No valid authorization header found."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        data = request.data
        if(not "latitude" in data or not "longitude" in data):
            return Response( status=status.HTTP_400_BAD_REQUEST)

        #latitude = float(data["latitude"])
        #longitude = float(data["longitude"])
        #data["location"] = Point(latitude,longitude)
        data["location"] = {"latitude":data["latitude"],"longitude":data["longitude"]}
        del data["latitude"]
        del data["longitude"]
        #Se setea como timestamp la fecha y hora del servidor
        data["timestamp"] = datetime.now()
        data["route"] = int(data["route"])
        serializer = StepSerializer(data=data, partial=True)
        print(data)
        if serializer.is_valid():
            serializer.save()
            response={}
            response["id"] = serializer.data["id"]
            return JsonResponse(response)
        print(serializer.errors)

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
        #se verifica primero que se haya adjuntado el token como header
        meta = request.META
        if('HTTP_AUTHORIZATION' not in meta or not User.objects.filter(token=meta['HTTP_AUTHORIZATION']).exists() or  
            int(User.objects.get(token=meta['HTTP_AUTHORIZATION']).role) != DELIVERY_MAN):
            return Response(
                data={
                    "message": "Authorization denied. No valid authorization header found."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        data = request.data
        #obtener usuario de acuerdo al token
        user = User.objects.get(token=meta['HTTP_AUTHORIZATION'])
        #se actualiza el estado del pedido a "en camino"
        purchase = Purchase.objects.get(pk=int(data["purchase"]))
        try:
            print("La ruta existe")
            route_id = purchase.route.id
            response={}
            response["id"] = route_id
            return JsonResponse(response)
        except ObjectDoesNotExist:
           # purchase.status = TO_BE_SENT
           # purchase.save()
            Purchase.objects.filter(id=int(data['purchase'])).update(status=TO_BE_SENT)
            #se crea la ruta
            data["user"] = user.id
            serializer = RouteSerializer(data=data, partial=True)
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
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        route = self.get_object(pk)
        route.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
