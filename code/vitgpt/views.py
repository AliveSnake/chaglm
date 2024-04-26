import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import CustomUser
from vitgpt.models import VIT,Image
from vitgpt.serializers import VITSerializer
from message.models import Message,MessageText
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse 
import json
import sys
sys.path.append("..")
current_directory = os.getcwd()
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
sys.path.append(parent_directory)
from model.vit.vitgpt import efficientvit
efficientvit_path = os.path.abspath(os.path.join(current_directory, '..', 'model', 'vit'))

sys.path.append(efficientvit_path)
class VITListCreateAPIView(APIView):


    def get(self, request):
        vit_objects = VIT.objects.all()
        serializer = VITSerializer(vit_objects, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = VITSerializer(data=request.data)
        if serializer.is_valid():
            note = serializer.save()

            current_directory = os.getcwd()
            image_directory = os.path.join(current_directory, 'static', 'vit')


            user_id = serializer.validated_data['user_id'].phone
            user = CustomUser.objects.get(phone=user_id)
            serializer.save(user_id=user)

            images = request.FILES.getlist('images')
            for image in images:
                Image.objects.create(note=note, image=image)  # 创建NoteImage对象，并手动设置相关字段
                

            image_path = None
            uploaded_file = request.FILES.get('images')
            str0 = uploaded_file.name.replace(" ", "_").replace("(","").replace(")","")
            image_path = os.path.join(image_directory,str0)
            result_text,his_text=efficientvit(image_path)
            note.text = result_text

            # his = f'[AI：{result_text}]'
            his = his_text
            # test_message = [{'role': 'user', 'content': '目前历史对话记录功能未链接大语言模型。'}, {'role': 'assistant', 'metadata': '', 'content': '历史记录功能链接大语言模型之后便输出正常。'}]
            Message.objects.create(user_id=user,image=image,reply=result_text,history=his)
            # Message.objects.create(user_id=user,image=image,reply=result_text,history=test_message)
            note.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VITDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return VIT.objects.get(pk=pk)
        except VIT.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        vit_object = self.get_object(pk)
        serializer = VITSerializer(vit_object)
        return Response(serializer.data)

    def put(self, request, pk):
        vit_object = self.get_object(pk)
        serializer = VITSerializer(vit_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vit_object = self.get_object(pk)
        vit_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VIT_Websocket(APIView):
    def post(self, request,pk):
        test = self.test()
        data = request.data
        user = str(pk)
        channel_layer = get_channel_layer()

        history = Message.objects.get(user_id=user).history
        history_list = json.loads(history)
        if not history_list:
            history = Message.objects.get(user_id=user).reply
        
        message = test(history)
        
        Message.objects.get(user_id=user).history.update(history + message)

        self.send_message_to_websocket(message)

        # 其他代码...

        return JsonResponse({"status": "success"})

    def send_message_to_websocket(self, message):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "dialog_group", {"type": "send_message", "message": message}
        )

    def test(history):
        return '1'