import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HelloWorld.settings')
import django
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from HelloWorld.routing import vitgpt_websocket_urlpatterns


# 获取默认的Django ASGI应用程序
django_asgi_application = get_asgi_application()

# 添加WebSocket路由配置
application = ProtocolTypeRouter(
    {
        "http": django_asgi_application,
        "websocket": URLRouter( 
            vitgpt_websocket_urlpatterns
        ),
    }
)