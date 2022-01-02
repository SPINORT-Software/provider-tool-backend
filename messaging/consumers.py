import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import SyncConsumer
from asgiref.sync import sync_to_async
from .models import Message


class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # room_name_raw = user1UUID___user2UUID
        room_type_raw = self.scope['url_route']['kwargs']['socket_type']

        self.room_name = "ROOM_TYPE_CHAT"
        self.room_group_name = 'socket_group_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)

        message = data['message']
        message_type = data['message_type']
        sender = data['sender']
        recipient = data['recipient']
        sent_at = data['sent_at']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'recipient': recipient,
                'message_type': message_type,
                'sent_at': sent_at
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @sync_to_async
    def save_message(self, message):
        pass
        # Message.objects.create()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Notification consumer")
        await self.accept()


class EchoConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        self.send({
            "type": "websocket.send",
            "text": event["text"],
        })