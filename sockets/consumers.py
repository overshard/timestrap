import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from core.models import Task, Client, Project


class UpdateConsumer(AsyncWebsocketConsumer):
    # TODO: This really should use channel layers and not something as janky as
    # storing everything currently avaliable on connection and double check on
    # polling. That defeats the purpose of using websockets.

    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        await self.send(json.dumps({
            'tasks': await self.get_task_count(),
            'clients': await self.get_client_count(),
            'projects': await self.get_project_count(),
        }))

    @database_sync_to_async
    async def get_task_count(self):
        return Task.objects.count()

    @database_sync_to_async
    async def get_client_count(self):
        return Client.objects.filter(archive=False).count()

    @database_sync_to_async
    async def get_project_count(self):
        return Project.objects.filter(archive=False).count()
