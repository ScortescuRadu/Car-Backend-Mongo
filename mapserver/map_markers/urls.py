from django.urls import path
from .views import MarkerListCreateView, MarkerDetailView, MarkersScanView, ReserveMarkerView, CancelReservationView, AddMarkerView, MarkerOccupiedStatusView, ClosestAvailableMarkerView

urlpatterns = [
    path('markers/', MarkerListCreateView.as_view(), name='marker-list-create'),
    path('markers/<int:pk>/', MarkerDetailView.as_view(), name='marker-detail'),
    path('scan/', MarkersScanView.as_view(), name='markers_scan'),
    path('reserve-marker/<int:pk>/', ReserveMarkerView.as_view(), name='reserve-marker'),
    path('cancel-reservation/<int:pk>/', CancelReservationView.as_view(), name='cancel-reservation'),
    path('add-marker/', AddMarkerView.as_view(), name='add-marker'),
    path('status/<int:marker_id>/', MarkerOccupiedStatusView.as_view(), name='marker-status'),
    path('closest-available/', ClosestAvailableMarkerView.as_view(), name='closest-available-marker'),
]