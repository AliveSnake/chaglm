# routing.py
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HelloWorld.settings')
import django
django.setup()
from django.urls import re_path, path
from vitgpt.consumers import VIT_Web

vitgpt_websocket_urlpatterns = [ 
    re_path(r'ws/vitgpt/(?P<group_name>\w+)/$', VIT_Web.as_asgi()),  
]
