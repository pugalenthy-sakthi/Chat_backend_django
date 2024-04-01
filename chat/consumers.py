from channels.generic.websocket import AsyncWebsocketConsumer
from djangochat.common import JWT, Responses, response_sender, get_random_id
from http import HTTPStatus
import json
from auth_app.models import Activity, Users
from .models import ChatActivity, Chats
from asgiref.sync import sync_to_async
from urllib.parse import parse_qs
from django.db import transaction

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            query = self.scope.get('query_string')
            query = parse_qs(query.decode('utf-8'))
            user1_email = query.get('user')[0]
            user2_email = query.get('to')[0]

            user1 = await sync_to_async(Users.objects.get)(email=user1_email)
            user2 = await sync_to_async(Users.objects.get)(email=user2_email)

            if user1 is None or user2 is None:
                raise Exception('Invalid Data')

            chatactivity = await sync_to_async(self.get_or_create_chatactivity)(user1, user2)

            self.room_group_name = chatactivity.room_id
            await self.channel_layer.group_add(
                self.room_group_name,self.channel_name
            )
            await self.accept()
        except Exception as e:
            print(e)
            await self.handle_exception(e)

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'data':text_data
            }
            
        )
    
    async def chat_message(self, data):
        await self.send(text_data=data['data'])
   
    async def handle_exception(self, exception):
        await self.close(code=1008)

    def get_or_create_chatactivity(self, user1, user2):
        with transaction.atomic():
            chatactivity = ChatActivity.objects.filter(user_1=user1, user_2=user2).first()
            if chatactivity is None:
                chatactivity = ChatActivity.objects.filter(user_1=user2, user_2=user1).first()
                if chatactivity is None:
                    chatactivity = ChatActivity()
                    chatactivity.room_id = get_random_id()
                    chatactivity.save()
                    chatactivity.user_1.set([user1])
                    chatactivity.user_2.set([user2])
                    chatactivity.save()
        return chatactivity
