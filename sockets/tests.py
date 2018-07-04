import pytest

from django.core.management import call_command

from channels.testing import WebsocketCommunicator

from .consumers import UpdateConsumer


call_command('migrate', verbosity=0)
call_command('fake', iterations=1, verbosity=0)


@pytest.mark.asyncio
async def test_websocket(self):
    communicator = WebsocketCommunicator(UpdateConsumer, '/socket/')
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.send_to(text_data="hello")
    response = await communicator.receive_from()
    assert response == "hello"
    await communicator.disconnect()
