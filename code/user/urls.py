from django.urls import path

from . import views

urlpatterns = [
    path("customusers", views.CustomUserList.as_view(), name="create_customuser"),
    path("customusers/<str:pk>", views.CustomUserDetail.as_view(), name="get_update_customuser"),
]