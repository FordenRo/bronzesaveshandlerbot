import re
import time

from aiogram import Router
from aiogram.types import Message, MessageEntity

from filters.reply import ReplyFilter
from utils.standoff import BoughtItem, GivenItem

router = Router()
thread_id = 98


@router.message(ReplyFilter(276))
async def bought_handler(message: Message):
    await message.delete()

    entity: MessageEntity = next(filter(lambda entity: entity.type == 'pre', message.reply_to_message.entities))
    entity_text = entity.extract_from(message.reply_to_message.text)
    items: [BoughtItem] = BoughtItem.parse_all(entity_text)

    arg = message.text.split()[0]
    if arg == 'del':
        index = int(message.text.split()[1]) - 1
        items.pop(index)
    elif arg == 'help':
        await message.answer('type "name" add? price amount? date?')
        return
    else:
        match = re.match(
            '(?P<type>[a-zA-Z\\-]+) "(?P<name>.+)" ?(?P<add>[a-zA-Z]*) (?P<price>[0-9.]+) ?(?P<amount>\\d*) ?(?P<date>[0-9.]*)',
            message.text).groupdict()
        name = ' '.join([match['type'].upper(), f'"{match['name'].capitalize()}"', match['add'].upper()])
        price = float(match['price'])
        amount = int(match['amount'] or 1)
        date = match['date'] or time.strftime('%d.%m')
        new_item = BoughtItem(name, price, amount, date)

        items.insert(0, new_item)

    text = f'Покупки\n\n<pre>{BoughtItem.items_to_text(items)}</pre>'
    await message.reply_to_message.edit_text(text, parse_mode='html')


@router.message(ReplyFilter(251))
async def given_handler(message: Message):
    await message.delete()

    entity: MessageEntity = next(filter(lambda entity: entity.type == 'pre', message.reply_to_message.entities))
    entity_text = entity.extract_from(message.reply_to_message.text)
    items: [GivenItem] = GivenItem.parse_all(entity_text)

    arg = message.text.split()[0]
    if arg == 'del':
        index = int(message.text.split()[1]) - 1
        items.pop(index)
    elif arg == 'help':
        await message.answer('id nickname? amount date?')
        return
    else:
        match = re.match('(?P<id>\\d+) ?(?P<nickname>\\w*) (?P<amount>[0-9.]+) ?(?P<date>[0-9.]*)',
                         message.text).groupdict()
        match['amount'] = float(match['amount'])
        match['id'] = int(match['id'])
        match['date'] = match['date'] or time.strftime('%d.%m')
        new_item = GivenItem(**match)

        items.insert(0, new_item)

    text = f'Давал голду\n\n<pre>{GivenItem.items_to_text(items)}</pre>'
    await message.reply_to_message.edit_text(text, parse_mode='html')
