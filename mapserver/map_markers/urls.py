from django.urls import path
from .views import MarkerListCreateView, MarkerDetailView, MarkersScanView

urlpatterns = [
    path('markers/', MarkerListCreateView.as_view(), name='marker-list-create'),
    path('markers/<int:pk>/', MarkerDetailView.as_view(), name='marker-detail'),
    path('scan/', MarkersScanView.as_view(), name='markers_scan'),
]