import os
from django.core.management import execute_from_command_line

from django.db import models
from .sto import mystorage
from user.models import CustomUser
# Create your models here.
class VIT(models.Model):
    user_id =models.ForeignKey(CustomUser,on_delete=models.CASCADE,help_text="用户ID",verbose_name="用户ID")
    created_datetime = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updated_datetime = models.DateTimeField(auto_now=True,verbose_name="更新时间")
    text = models.TextField(null=True,blank=True,help_text="文本",verbose_name="文本")

class Image(models.Model):
    note = models.ForeignKey(VIT, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/vit', help_text="图片", verbose_name="图片")

       