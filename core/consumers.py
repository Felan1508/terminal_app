# terminal_app/consumers.py
import asyncio
import subprocess
from channels.generic.websocket import AsyncWebsocketConsumer

class TerminalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        process = await asyncio.create_subprocess_shell(
            text_data,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        while True:
            line = await process.stdout.readline()
            if not line:
                break
            await self.send(line.decode())

        await process.wait()
