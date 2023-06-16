import datetime
import json
import time

import aio_pika


# import pika


class LogsService:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def send_message(self, body):
        self.connection = await aio_pika.connect_robust(host='localhost', port=5672)

        async with self.connection:
            channel = await self.connection.channel()

            await channel.default_exchange.publish(
                message=aio_pika.Message(body=json.dumps(body).encode()),
                routing_key='queue'
            )
