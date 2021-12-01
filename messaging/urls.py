from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/<str:socket_type>/', consumers.MessageConsumer.as_asgi())
]

