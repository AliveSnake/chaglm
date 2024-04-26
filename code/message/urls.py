from django.urls import path,include
from message import views



urlpatterns = [
    path("list/",views.MessageList.as_view()),
    path("list/<str:pk>/",views.MessageDetail.as_view()),
    path("list/user/<str:pk>/",views.UserMessageList.as_view()),
]
