from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.formatting import Pre, Text

from filters.command import MyCommand

router = Router()


@router.message(MyCommand('tohtml', description='Message to HTML'))
async def tohtml(message: Message):
    await message.answer(**Pre(message.reply_to_message.html_text, language='HTML').as_kwargs())


@router.message(MyCommand('fromhtml', description='Parse message with HTML'))
async def fromhtml(message: Message):
    await message.answer(message.reply_to_message.text, parse_mode='html')
