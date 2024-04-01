from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from .consumers import MyConsumer

websocket_urlpattern = [
            path('ws/chat', MyConsumer.as_asgi()),
            ]
