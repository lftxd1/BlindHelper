from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import json, time

# 这里除了 WebsocketConsumer 之外还有
# JsonWebsocketConsumer
# AsyncWebsocketConsumer
# AsyncJsonWebsocketConsumer
# WebsocketConsumer 与 JsonWebsocketConsumer 就是多了一个可以自动处理JSON的方法
# AsyncWebsocketConsumer 与 AsyncJsonWebsocketConsumer 也是多了一个JSON的方法
# AsyncWebsocketConsumer 与 WebsocketConsumer 才是重点
# 看名称似乎理解并不难 Async 无非就是异步带有 async / await
# 是的理解并没有错,但对与我们来说他们唯一不一样的地方,可能就是名字的长短了,用法是一模一样的
# 最夸张的是,基类是同一个,而且这个基类的方法也是Async异步的

socket_list = []


class ChatService(AsyncWebsocketConsumer):

    async def connect(self):  # 连接时触发
        self.room_name = "house"
        self.room_group_name = self.room_name  # 直接从用户指定的房间名称构造Channels组名称，不进行任何引用或转义。

        # 将新的连接加入到群组
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await push("测试发消息")
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'system_message',
        #         'message': "123"
        #     }
        # )

    async def disconnect(self, close_code):  # 断开时触发
        # 将关闭的连接从群组中移除
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):  # 接收消息时触发

        message = text_data

        # 信息群发

        # await self.push("123")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'system_message',
                'message': message
            }
        )

    # Receive message from room group
    async def system_message(self, event):
        print(event)
        message = event['message']

        # Send message to WebSocket单发消息
        await self.send(text_data=json.dumps({
            'message': message
        }))


async def push( message):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        "house",
        {
            'type': 'system_message',
            'message': message
        }
    )

