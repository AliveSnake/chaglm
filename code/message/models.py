import os
from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grape.settings")
from django.db import models
from user.models import CustomUser
import uuid

# Create your models here.
class Message(models.Model):
    user_id =models.ForeignKey(CustomUser,on_delete=models.CASCADE,help_text="用户ID",verbose_name="用户ID")
    uuid =models.UUIDField(help_text="消息记录uuid",verbose_name="消息记录uuid",primary_key=True,default=uuid.uuid4,editable=True)
    image = models.ImageField(upload_to='grape/static/message', help_text="图片", verbose_name="图片")
    reply = models.TextField(null=True,blank=True,help_text="总文本", verbose_name="总文本")
    created_datetime = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    history = models.TextField(null=True,blank=True,help_text="历史记录", verbose_name="历史记录")

    class  Meta:
        verbose_name = '消息记录'
        verbose_name_plural = verbose_name
    
    #对于模型类的实例，使用uuid
    def __str__(self):
        return self.uuid
    
class MessageText(models.Model):
    message = models.ForeignKey(Message, related_name='texts', on_delete=models.CASCADE)
    role = models.CharField(max_length=255,blank=True, help_text="角色", verbose_name="角色")
    text = models.TextField(null=True,blank=True,help_text="文本", verbose_name="文本")

    def __str__(self):
        return f"{self.role}: {self.text}"    