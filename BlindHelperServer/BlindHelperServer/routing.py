from channels.routing import ProtocolTypeRouter,URLRouter
from MouleOne.urls import websocket_url
application = ProtocolTypeRouter({
    "websocket": URLRouter(
        websocket_url
    )
})