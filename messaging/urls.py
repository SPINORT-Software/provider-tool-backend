from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/<str:socket_type>/', consumers.MessageConsumer.as_asgi()),

    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),

    path('ws/echo/', consumers.EchoConsumer.as_asgi()),
]

