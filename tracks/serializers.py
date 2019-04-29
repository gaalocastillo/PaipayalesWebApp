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
	location = PointField()

	class Meta:
		model = Step
		fields = ('location', 'timestamp', 'route')

class RouteSerializer(serializers.ModelSerializer):
	user = serializers.SlugRelatedField(many=False,queryset=User.objects.all(),slug_field='id')
	steps = StepSerializer(many=True)

	class Meta:
		model = Route
		fields = ('distance', 'init_time', 'user', 'steps')
