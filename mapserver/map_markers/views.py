from django.shortcuts import render
from rest_framework import generics
from .models import Marker
from .serializers import MarkerSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import math

def haversine(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

# Create your views here.
class MarkerListCreateView(generics.ListCreateAPIView):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer


class MarkerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer


class MarkersScanView(generics.ListAPIView):
    serializer_class = MarkerSerializer

    def get_queryset(self):
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')
        distance = self.request.query_params.get('distance')

        if lat is None or lon is None or distance is None:
            raise ValidationError("Latitude, longitude, and distance parameters are required.")
        
        try:
            lat = float(lat)
            lon = float(lon)
            distance = float(distance)
        except ValueError:
            raise ValidationError("Latitude, longitude, and distance must be valid numbers.")

        def haversine(lat1, lon1, lat2, lon2):
            lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            r = 6371  # Radius of earth in kilometers
            return c * r

        queryset = Marker.objects.all()
        filtered_queryset = []

        for marker in queryset:
            distance_to_marker = haversine(lat, lon, marker.lat, marker.lng)
            if distance_to_marker <= distance:
                filtered_queryset.append(marker)

        return filtered_queryset


class ReserveMarkerView(generics.UpdateAPIView):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.is_reserved:
            return Response({"error": "Marker is already reserved"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data={'is_reserved': True}, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class CancelReservationView(generics.UpdateAPIView):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.is_occupied:
            return Response({"error": "Marker is occupied and cannot be canceled"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data={'is_reserved': False}, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class AddMarkerView(generics.CreateAPIView):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

    def create(self, request, *args, **kwargs):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        is_occupied = request.data.get('is_occupied', False)

        print(f"Received latitude: {latitude}, longitude: {longitude}, is_occupied: {is_occupied}")

        try:
            # Check if a marker exists at the exact latitude and longitude
            # if Marker.objects.filter(lat=latitude, lng=longitude).exists():
            #     print("Marker already exists at this location")
            #     return Response({'error': 'Marker already exists at this location'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the marker with the is_occupied field
            marker = Marker(lat=latitude, lng=longitude, is_occupied=is_occupied)
            marker.save()

            serializer = self.get_serializer(marker)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error occurred while creating marker: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarkerOccupiedStatusView(APIView):
    def get(self, request, marker_id):
        try:
            marker = Marker.objects.get(id=marker_id)
            return Response({'is_occupied': marker.is_occupied}, status=status.HTTP_200_OK)
        except Marker.DoesNotExist:
            return Response({'error': 'Marker not found'}, status=status.HTTP_404_NOT_FOUND)


class ClosestAvailableMarkerView(APIView):
    def get(self, request):
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lng')

        if lat is None or lon is None:
            return Response({'error': 'Latitude and longitude are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return Response({'error': 'Invalid latitude or longitude'}, status=status.HTTP_400_BAD_REQUEST)

        closest_marker = None
        min_distance = float('inf')

        try:
            all_markers = Marker.objects.all()  # Fetch all markers
            available_markers = [marker for marker in all_markers if not marker.is_occupied]  # Filter in Python

            for marker in available_markers:
                distance = haversine(lat, lon, marker.lat, marker.lng)
                if distance < min_distance:
                    min_distance = distance
                    closest_marker = marker

            if closest_marker:
                serializer = MarkerSerializer(closest_marker)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No available markers found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)