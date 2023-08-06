import asyncio
import time

import discord
from langchain.callbacks.base import AsyncCallbackHandler


class StreamMessageHandler(AsyncCallbackHandler):
    def __init__(self, event_loop):
        super().__init__()
        self._event_loop = event_loop
        self._current_message = None
        self.message_content = ""
        self.token_queue = asyncio.Queue()
        self.batch_size = 10
        self.batch_time = 1.0  # seconds
        self.last_batch_time = time.time()

    @property
    def current_message(self):
        return self._current_message

    @current_message.setter
    def current_message(self, message:discord.Message):
        self.message_content = ""
        self._current_message = message

    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        if self.current_message:
            await self.token_queue.put({'token': token,
                                        'timestamp': time.perf_counter_ns()})

    async def _run(self):
        while True:
            token_payloads = []
            start_time = time.time()
            while len(token_payloads) < self.batch_size and time.time() - start_time < self.batch_time:
                try:
                    token_payload = await asyncio.wait_for(self.token_queue.get(), timeout=1)
                    token_payloads.append(token_payload)
                except asyncio.TimeoutError:
                    continue

            if token_payloads:
                tokens = [token_payload['token'] for token_payload in token_payloads]
                timestamps = [token_payload['timestamp'] for token_payload in token_payloads]
                self.message_content += ''.join(tokens)
                if self.current_message and len(self.message_content) > 0:
                    await self.current_message.edit(content=self.message_content)

    def start(self):
        self.task = asyncio.ensure_future(self._run())

    def stop(self):
        self.task.cancel()
