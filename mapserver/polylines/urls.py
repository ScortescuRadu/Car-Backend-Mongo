from django.urls import path
from .views import PolylineListCreateView, PolylineDetailView

urlpatterns = [
    path('', PolylineListCreateView.as_view(), name='polyline-list-create'),
    path('<int:pk>/', PolylineDetailView.as_view(), name='polyline-detail'),
]
