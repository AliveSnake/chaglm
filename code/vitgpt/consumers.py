import os
from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grape.settings")
import sys 
sys.path.append("..")
current_directory = os.getcwd()
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
efficientvit_path = os.path.abspath(os.path.join(current_directory, '..', 'model', 'vit'))
sys.path.append(efficientvit_path)
sys.path.append(parent_directory)
from model.vit.vitgpt1 import ChatAI
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import ast
from message.models import Message
from channels.db import database_sync_to_async
@database_sync_to_async
def get_message_instance(group_name):
    return Message.objects.filter(user_id=group_name).order_by('-created_datetime').first()

@database_sync_to_async
def save_message_instance(message_instance):
    message_instance.save()

class VIT_Web(AsyncWebsocketConsumer):
    def test(self, message, history):
        rep = message
        return rep

    async def connect(self):
        
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data = json.dumps({
            'message':text_data
        })
        
        if not text_data:
            # 空字符串错误处理
            error_message = "Empty message received. Please send a valid JSON object."
            await self.send(text_data=json.dumps({'error': error_message}))
            return
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']    # user input
        except json.JSONDecodeError as e:
            # JSON解码错误处理
            error_message = f"Invalid JSON data: {e}"
            await self.send(text_data=json.dumps({'error': error_message}))
            return
        except KeyError:
            # 缺少'message'字段错误处理
            error_message = "Invalid message format: missing 'message' field"
            await self.send(text_data=json.dumps({'error': error_message}))
            return
        
        message_instance = await get_message_instance(self.group_name)


        his_save = ast.literal_eval(message_instance.history)
        print('his_save:',his_save)

        # new_record = {'role': 'user', 'content': message}
        # his_save.append(new_record)

        # # 保存用户输入信息
        # message_instance.history = json.dumps(his_save)
        # await save_message_instance(message_instance) 

        reply,his = ChatAI(message=message,his=his_save)

        print('reply:',reply)
        print('his:',his)     

        # reply = self.test(message, message_instance.history)

        # 保存AI回复信息
        # message_instance.history = message_instance.history + f'AI:{reply}'
        message_instance.history = his
        await save_message_instance(message_instance)

        await self.send(text_data=json.dumps({
            'AI': reply,
        }))
        
    # Receive message from room group
    async def push_message(self, event):
        print(event)
        await self.send(text_data=json.dumps({
            "event": event['event']
        }))
        