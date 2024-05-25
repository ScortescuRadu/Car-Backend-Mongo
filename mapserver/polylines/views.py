from django.shortcuts import render
from rest_framework import generics
from .models import Polyline
from .serializers import PolylineSerializer
# Create your views here.

class PolylineListCreateView(generics.ListCreateAPIView):
    queryset = Polyline.objects.all()
    serializer_class = PolylineSerializer

class PolylineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Polyline.objects.all()
    serializer_class = PolylineSerializer