from django.shortcuts import render
from rest_framework import generics
from .models import GeoJsonFeature
from .serializers import GeoJsonFeatureSerializer

# Create your views here.
class GeoJsonFeatureListCreateView(generics.ListCreateAPIView):
    queryset = GeoJsonFeature.objects.all()
    serializer_class = GeoJsonFeatureSerializer

class GeoJsonFeatureDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GeoJsonFeature.objects.all()
    serializer_class = GeoJsonFeatureSerializer