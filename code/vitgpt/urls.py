from django.urls import path
from .views import VITListCreateAPIView, VITDetailAPIView

urlpatterns = [
    path('vit/', VITListCreateAPIView.as_view(), name='vit-list-create'),
    path('vit/<int:pk>/', VITDetailAPIView.as_view(), name='vit-detail'),
]
