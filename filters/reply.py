from aiogram.filters import Filter
from aiogram.types import Message


class ReplyFilter(Filter):
    def __init__(self, message_id: int):
        self.message_id = message_id

    async def __call__(self, message: Message):
        if not isinstance(message, Message):
            return False

        return message.reply_to_message.message_id == self.message_id
