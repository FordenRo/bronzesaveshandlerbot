from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.formatting import Pre, Text

from filters.command import MyCommand

router = Router()


class EditStates(StatesGroup):
    state = State()


@router.message(MyCommand('tohtml', description='Message to HTML'))
async def tohtml(message: Message):
    await message.answer(**Pre(message.reply_to_message.html_text, language='html').as_kwargs())


@router.message(MyCommand('fromhtml', description='Parse message with HTML'))
async def fromhtml(message: Message):
    await message.answer(message.reply_to_message.text, parse_mode='html')


@router.message(MyCommand('copy', description='Copy message'))
async def copy(message: Message):
    await message.answer(message.reply_to_message.html_text, parse_mode='html')


@router.message(MyCommand('del', description='Delete message'))
async def delete(message: Message):
    await message.reply_to_message.delete()


@router.message(MyCommand('edit', description='Edit message'))
async def edit(message: Message, state: FSMContext):
    last = await message.answer(**Text('Введите новое сообщение\n\nИсходное:\n',
                                       Pre(message.reply_to_message.html_text, language='html')).as_kwargs())
    await state.set_state(EditStates.state)
    await state.set_data({'message': message.reply_to_message, 'last': last})


@router.message(EditStates.state)
async def edit_state(message: Message, state: FSMContext):
    edit_message: Message = await state.get_value('message')
    last_message: Message = await state.get_value('last')
    await state.clear()
    await edit_message.edit_text(message.text, parse_mode='html')
    await last_message.delete()
    await message.delete()
