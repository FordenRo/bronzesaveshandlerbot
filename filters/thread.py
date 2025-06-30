from aiogram.filters import Filter
from aiogram.types import Message


class ThreadFilter(Filter):
    def __init__(self, thread_id: int):
        self.thread_id = thread_id

    async def __call__(self, message: Message):
        if not isinstance(message, Message):
            return False

        return message.message_thread_id == self.thread_id
