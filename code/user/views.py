from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from user.models import CustomUser
from django.contrib.auth.models import User
from django.conf import settings
from user.serializer import CustomUserSerializer
from rest_framework import generics
from rest_framework import status, viewsets, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.reverse import reverse_lazy
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class CustomUserList(generics.ListCreateAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=CustomUserSerializer
class CustomUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=CustomUserSerializer
    
    def delete(self,request,pk):
        User.objects.filter(username=pk).delete()
        CustomUser.objects.filter(pk=pk).delete()
        return Response("删除成功!")