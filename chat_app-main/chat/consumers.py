# consumers.py

import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from .models import Message
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        user1 = self.scope['user'].username
        user2 = self.room_name
        self.room_group_name = f"chat_{''.join(sorted([user1, user2]))}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'error': 'Formato JSON inválido'}))
            return

        message = text_data_json.get('message', '')
        file_data = text_data_json.get('file', None)      # base64 string
        file_name = text_data_json.get('file_name', None)
        file_type = text_data_json.get('file_type', None)

        sender = self.scope['user']
        receiver = await self.get_receiver_user(self.room_name)
        if receiver is None:
            await self.send(text_data=json.dumps({
                'error': 'El usuario receptor no existe.'
            }))
            return

        msg = await self.save_message(sender, receiver, message, file_data, file_name)

        file_url = msg.file.url if msg.file else None

        # Enviar mensaje a todos en el grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': sender.username,
                'receiver': receiver.username,
                'message': message,
                'file_url': file_url,
                'file_name': file_name,
                'file_type': file_type,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'sender': event['sender'],
            'receiver': event['receiver'],
            'message': event['message'],
            'file_url': event.get('file_url'),
            'file_name': event.get('file_name'),
            'file_type': event.get('file_type'),
        }))

    @sync_to_async
    def save_message(self, sender, receiver, message, file_data=None, file_name=None):
        msg = Message(sender=sender, receiver=receiver, content=message)
        if file_data and file_name:
            try:
                # file_data esperado en formato: data:<mime-type>;base64,<data>
                header, encoded = file_data.split(';base64,')
                data = ContentFile(base64.b64decode(encoded), name=file_name)
                msg.file = data
            except Exception as e:
                # Opcional: log error
                pass
        msg.save()
        return msg

    @sync_to_async
    def get_receiver_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
