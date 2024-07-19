from rest_framework import serializers
from .models import City

class CitySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city', 'count']