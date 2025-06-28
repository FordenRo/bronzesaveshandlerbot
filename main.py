from asyncio import run

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import BotCommand, Message

from filters.command import MyCommand
from handlers import standoff, htmlparser

dispatcher = Dispatcher()


@dispatcher.message(CommandStart())
async def start(message: Message):
    print(message.chat.id)
    print(message.message_thread_id)


async def main():
    bot = Bot('8084365036:AAFgTAGeCYJP-zOw_DMV7zpm3ZiWsICkggo')

    dispatcher.include_routers(standoff.router,
                               htmlparser.router)

    await bot.set_my_commands([BotCommand(command=command.commands[0], description=command.description)
                               for command in MyCommand.command_list if command.prefix == '/'])

    await dispatcher.start_polling(bot)


run(main())
