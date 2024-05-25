from django.urls import path
from .views import GeoJsonFeatureListCreateView, GeoJsonFeatureDetailView

urlpatterns = [
    path('geojson/', GeoJsonFeatureListCreateView.as_view(), name='geojsonfeature-list-create'),
    path('geojson/<int:pk>/', GeoJsonFeatureDetailView.as_view(), name='geojsonfeature-detail'),
]