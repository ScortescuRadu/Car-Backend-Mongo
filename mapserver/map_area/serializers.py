from rest_framework import serializers
from .models import GeoJsonFeature

class GeoJsonFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoJsonFeature
        fields = '__all__'