import json

from channels.generic.websocket import WebsocketConsumer

from core.models import Task, Client, Project


class UpdateConsumer(WebsocketConsumer):
    # TODO: This really should use channel layers and not something as janky as
    # storing everything currently avaliable on connection and double check on
    # polling. That defeats the purpose of using websockets.

    tasks = 0
    clients = 0
    projects = 0

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        self.tasks = Task.objects.count()
        self.clients = Client.objects.filter(archive=False).count()
        self.projects = Project.objects.filter(archive=False).count()

        self.send(json.dumps({
            'tasks': self.tasks,
            'clients': self.clients,
            'projects': self.projects,
        }))
