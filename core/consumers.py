# consumers.py
import asyncio
import shlex
from channels.generic.websocket import AsyncWebsocketConsumer
import uuid
import datetime
import os

class TerminalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.process = None
        self.stop_event = asyncio.Event()
        self.stream_task = None
        await self.send(text_data="Connected to terminal.\n")

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected with code: {close_code}")
        await self._stop_process()

        if hasattr(self, "log_path"):
            try:
                with open(self.log_path, "a") as f:
                    f.write(f"\n⛔ WebSocket connection closed. Code: {close_code}\n")
                    f.flush()
                    os.fsync(f.fileno())
            except Exception as e:
                print(f"Error writing to log file during disconnect: {e}")


    async def receive(self, text_data):
        print("Received:", text_data)

        if text_data.strip() == "__STOP__":
            print(">>> STOP command received!")
            await self.send("⛔ Stopping process...\n")
            await self._stop_process()
            return

        # Start new command
        if self.process and self.process.returncode is None:
            await self.send("A process is already running. Please stop it first.\n")
            return

        try:
            args = shlex.split(text_data)
            self.stop_event.clear()

            self.process = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )

            self.stream_task = asyncio.create_task(self._stream_output())

        except Exception as e:
            await self.send(f"❌ Error: {str(e)}\n")
            self.process = None

   

    async def _stream_output(self):
        # Create logs directory with timestamped subfolders
        date_folder = datetime.datetime.now().strftime("day(%d-%m-%Y)")
        logs_dir = os.path.join("logs", date_folder)
        os.makedirs(logs_dir, exist_ok=True)

        filename = f"{uuid.uuid4().hex}_session.txt"
        filepath = os.path.join(logs_dir, filename)
        self.log_path = filepath

        try:
            with open(filepath, "w") as f:
                while not self.stop_event.is_set():
                    line = await self.process.stdout.readline()
                    if not line:
                        break
                    decoded_line = line.decode()
                    await self.send(decoded_line)
                    f.write(decoded_line)
                    f.flush()
        except Exception as e:
            # Internal server-side error
            error_msg = f"\n❌ Internal error: {str(e)}\n"
            await self.send(error_msg)

            with open(filepath, "a") as f:
                f.write(error_msg)
                f.flush()
        finally:
            await self.send("✅ Process finished.\n")
            with open(filepath, "a") as f:
                f.write("✅ Process finished.\n")



    async def _stop_process(self):
        if self.process and self.process.returncode is None:
            self.stop_event.set()
            self.process.kill()
            await self.process.wait()
            if self.stream_task:
                await self.stream_task
            self.process = None
