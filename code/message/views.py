from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Message, MessageText
from .serializers import MessageSerializer, MessageTextSerializer
from rest_framework.views import APIView
from user.models import CustomUser

class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    
class UserMessageList(APIView):
    def get(self,request,pk):
        ## 得到该用户下所有消息记录
        obj = Message.objects.filter(user_id=pk)
        if not obj:
            return Response(data={"msg":"没有该用户的消息记录信息"},status=status.HTTP_404_NOT_FOUND)
        s = MessageSerializer(instance=obj,many=True,)
        return Response(s.data,status=status.HTTP_200_OK) 
    
    def delete(self,request,pk):
         ## 删除该用户下所有的消息记录
        obj = Message.objects.filter(user_id=pk)
        if not obj:
            return Response(data={"msg":"没有该用户的消息记录信息"},status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
