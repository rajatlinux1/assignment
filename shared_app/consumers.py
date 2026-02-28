import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # We will extract the schema_name from the URL to join a tenant-specific broadcast group
        self.schema_name = self.scope["url_route"]["kwargs"].get(
            "schema_name", "public"
        )
        self.room_group_name = f"notifications_{self.schema_name}"

        print("schema_name == ", self.schema_name)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from room group
    async def send_notification(self, event):
        message = event["message"]
        print("message == ", message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
