import re
import time

from aiogram import Bot, Router
from aiogram.types import Message, MessageEntity

from filters.reply import ReplyFilter

router = Router()
thread_id = 98


@router.message(ReplyFilter(209))
async def registership(message: Message):
    await message.delete()

    pattern = 'Покупки\n\n<pre>{}</pre>'

    entity: MessageEntity = next(filter(lambda entity: entity.type == 'pre', message.reply_to_message.entities))
    entity_text = entity.extract_from(message.reply_to_message.text)

    if message.text.split()[0] == 'del':
        index = int(message.text.split()[1]) - 1
        skins = entity_text.split('\n\n')
        skins.pop(index)
        await message.reply_to_message.edit_text(f'Покупки\n\n<pre>{"\n\n".join(skins)}</pre>')
        return

    skin = re.match('(\\w+) "(\\w+)" ?(\\w*) ([0-9.]+)', message.text).groups()

    title = f'{skin[0].upper()} "{skin[1].capitalize()}"{f" {skin[2].upper()}" if skin[2] else ""}'
    footer = f'{f"{float(skin[3]):.2f} G":<11s}{time.strftime("%d.%m %H:%M"):>{len(title) - 11}s}'
    text = f'Покупки\n\n<pre>{title:^22s}\n{footer}\n\n{entity_text}</pre>'

    await message.reply_to_message.edit_text(text, parse_mode='html')
