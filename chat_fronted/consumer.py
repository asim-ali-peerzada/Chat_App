import json
from channels.generic.websocket import AsyncWebsocketConsumer
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'chat_room'
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        username = text_data_json.get('username')
        time = text_data_json.get('time')
        typing = text_data_json.get('typing')

        if message:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'time': time
                }
            )
        elif typing is not None:
            # Send typing status to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_status',
                    'username': username,
                    'typing': typing
                }
            )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        time = event['time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'time': time,
            'sound': 'static/sound/notification.mp3'
        }))

    async def typing_status(self, event):
        username = event['username']
        typing = event['typing']

        # Send typing status to WebSocket
        await self.send(text_data=json.dumps({
            'username': username,
            'typing': typing
        }))
