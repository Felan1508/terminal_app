import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.wsgi import get_wsgi_application
from django.core.asgi import get_asgi_application
from whitenoise import WhiteNoise
import core.routing

 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
 
# Tạo WSGI app để gói trong WhiteNoise
wsgi_app = get_wsgi_application()
wsgi_with_static = WhiteNoise(wsgi_app)
 
# Gói lại bằng ASGI để nhúng vào ProtocolTypeRouter
django_asgi_app = get_asgi_application()
 
application = ProtocolTypeRouter({
    "http": django_asgi_app,  # sử dụng get_asgi_application(), KHÔNG override call
    "websocket": AuthMiddlewareStack(
        URLRouter(
            core.routing.websocket_urlpatterns 
            
        )
    ),
})
 
 