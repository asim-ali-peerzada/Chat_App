from django.urls import path, include
from chat_fronted.consumer import ChatConsumer


# the empty string routes to ChatConsumer, which manages the chat functionality.
websocket_urlpatterns = [
    path("", ChatConsumer.as_asgi()),
]