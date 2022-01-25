import json
from channels.generic.websocket import AsyncWebsocketConsumer
from authentication.models import User
from channels.db import database_sync_to_async
from .models import Message
import logging

logger = logging.getLogger(__name__)

@database_sync_to_async
def save_message(message_data):
    try:
        logger.info(f"Saving Message received {message_data}")
        message = Message(
            body=message_data['message'],
            sender=User.objects.filter(username=message_data['sender']).first(),
            recipient=User.objects.filter(username=message_data['recipient']).first()
        )
        message.save()
    except Exception as e:
        logger.error(f"Exception occured while saving message: {str(e)}")


class MessageConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        self.room_group_name = "MESSAGING"
        super(MessageConsumer, self).__init__()

    async def connect(self):
        if self.scope['user']:
            connected_user = self.scope['user']
            logger.info(f"============================= Connected user: {connected_user.username}")
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            await self.send(text_data=json.dumps({'status': 'MESSAGING_CONNECTED'}))
        else:
            # Reject the connection
            await self.close()
            return

    async def disconnect(self, close_code):
        if self.scope['user']:
            logger.info("Disconnected")
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        else:
            await self.close(close_code)

    # Receive message from WebSocket Client
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_keys = ('message', 'message_type', 'sender', 'recipient', 'sent_at')

        # All the keys in message data are required for processing
        if all(message_key in data for message_key in message_keys):
            message = data['message']
            message_type = data['message_type']
            sender = data['sender']
            recipient = data['recipient']
            sent_at = data['sent_at']

            event_data =   {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'recipient': recipient,
                'message_type': message_type,
                'sent_at': sent_at
            }

            # Send message to room group
            logger.info("Received message")
            await self.channel_layer.group_send(
                self.room_group_name,
                event_data
            )
            await save_message(event_data)

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Notification consumer")
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
