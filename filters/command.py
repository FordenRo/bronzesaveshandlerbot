from asyncio import create_task

from aiogram import Bot
from aiogram.filters import Command
from aiogram.filters.command import CommandException
from aiogram.types import Message


class MyCommand(Command):
    command_list: list['MyCommand'] = []

    def __init__(self, *commands, description: str = None, thread_id: int = None, prefix: str = '/'):
        super().__init__(*commands, prefix=prefix)

        self.prefix = prefix
        self.description = description
        self.thread_id = thread_id

        MyCommand.command_list += [self]

    async def __call__(self, message: Message, bot: Bot):
        if not isinstance(message, Message):
            return False

        text = message.text or message.caption
        if not text:
            return False

        try:
            command = await self.parse_command(text=text, bot=bot)
        except CommandException:
            return False
        print(message.text)

        if self.thread_id and message.message_thread_id != self.thread_id:
            await message.answer('Команда не может быть использована в этой теме')
            return False

        result = {"command": command}
        if command.magic_result and isinstance(command.magic_result, dict):
            result.update(command.magic_result)
        return result
