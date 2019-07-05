import json

from channels.generic.websocket import AsyncWebsocketConsumer


class UpdateConsumer(AsyncWebsocketConsumer):
    """
    Goes with our core signal that, on model update, sends a message to all
    channels in the group to sync the UI.
    """

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("sync_clients", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("sync_clients", self.channel_name)

    async def sync_clients_save(self, event):
        await self.send(json.dumps({"model": event["model"]}))

    async def sync_clients_delete(self, event):
        await self.send(json.dumps({"model": event["model"]}))
