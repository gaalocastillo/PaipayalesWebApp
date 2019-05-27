from .models import *
from inventory.models import User
from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField

class LastLocationSerializer(serializers.ModelSerializer):
	user = serializers.SlugRelatedField(many=False,queryset=User.objects.all(),slug_field='id', required=False)
	location = PointField()

	class Meta:
		model = LastLocation
		fields = ('location', 'timestamp', 'user')



class StepSerializer(serializers.ModelSerializer):
	route = serializers.SlugRelatedField(many=False,queryset=Route.objects.all(),slug_field='id', required=False)
	location = PointField()
	class Meta:
		model = Step
		fields = ('id', 'location','timestamp','route' )

class RouteSerializer(serializers.ModelSerializer):
	user = serializers.SlugRelatedField(many=False,queryset=User.objects.all(),slug_field='id')
	steps = StepSerializer(many=True,read_only=True)
	origin = PointField()
	destination = PointField()
	#purchase = serializers.IntegerField(max_length=255, min_length=4, validators=[])
	#purchase = serializers.SlugRelatedField(many=False,queryset=Purchase.objects.all(),slug_field='id', required=False)

	class Meta:
		model = Route
		#fields = ('id','distance', 'init_time', 'user', 'steps')
		fields = "__all__"