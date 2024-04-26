import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HelloWorld.settings")
from channels.generic.websocket import AsyncWebsocketConsumer
import json
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
            message = text_data_json['message']
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

        # 保存用户输入信息
        # message_instance.history = message_instance.history + f'YOU:{message}' 
        # await save_message_instance(message_instance)      

        reply = self.test(message, message_instance.history)

        # 保存AI回复信息
        test_message = [{'role': 'user', 'content': '目前历史对话记录功能未链接大语言模型。'}, {'role': 'assistant', 'metadata': '', 'content': '历史记录功能链接大语言模型之后便输出正常。'}]
        message_instance.history = test_message
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
        