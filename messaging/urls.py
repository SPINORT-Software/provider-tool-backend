from django.urls import path
from . import consumers
from .views import *

websocket_urlpatterns = [
    path('ws/chat/', consumers.MessageConsumer.as_asgi()),
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
]

urlpatterns = [
    path('history/<str:username>', MessagingViews.HistoryList.as_view()),
    path('share/', ShareViews.ShareObject.as_view()),
]