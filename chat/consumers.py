from chat.models import Chat, Message
import json
from django.utils import timezone
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


@database_sync_to_async
def get_chat(slug):
    return Chat.objects.get(slug=slug)


@database_sync_to_async
def save_message(chat, text, author):
    Message.objects.create(chat=chat, text=text, author=author)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["slug"]
        self.user = self.scope["user"]
        self.chat_obj = await get_chat(self.room_name)

        if not self.user.is_authenticated:
            self.send({"close": True})

        self.user = self.scope["user"]
        self.room_group_name = f"chat_{self.room_name}"
        # Join room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await save_message(self.chat_obj, message, self.user)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "username": self.user.username,
                "created_at": timezone.now().isoformat(),
                "message": message,
            },
        )

    async def chat_message(self, event):
        """
        Receive message from group
        """
        message = event["message"]
        username = event["username"]
        createdAt = event["created_at"]

        await self.send(
            text_data=json.dumps(
                {"message": message, "username": username, "createdAt": createdAt}
            )
        )
