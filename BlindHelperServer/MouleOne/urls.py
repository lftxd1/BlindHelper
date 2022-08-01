from MouleOne.chatService import ChatService
from django.urls import re_path
from django.urls import path
websocket_url = [
    re_path(r'^ws/', ChatService.as_asgi())
]