from aiogram import Router, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.deep_linking import create_start_link, decode_payload

import re
from loguru import logger
from bot_settings import bot
from utils.user_utils import get_sender_id
from keyboards.user_kybr import write_again_keybr, reply_keybr

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()


class User(StatesGroup):
    sender = State()
    reader = State()


@router.message(CommandStart())
async def start_hand(msg: types.Message, command: CommandObject, state: FSMContext):
    user_id = command.args
    if user_id:
        await state.set_state(User.sender)
        await state.update_data(user_id=decode_payload(user_id))
        return await msg.answer('Отлично! Теперь напиши своё сообщение: ')
    link = await create_start_link(bot, payload=msg.from_user.id, encode=True)
    await msg.answer(f'Твоя ссылка для анонимных сообщений: {link}')


@router.message(User.sender)
async def send_msg(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(data['user_id'], 'У тебя новое сообщение!')
    await bot.send_message(data['user_id'], msg.text)
    await msg.answer(text='Хочешь написать еще что-нибудь?', reply_markup=write_again_keybr())


@router.message(User.reader)
async def send_reply(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(data['sender_id'], 'Сообщение отправлено!')


@router.callback_query()
async def cb_handler(cb: types.CallbackQuery, state: FSMContext):
    if cb.data == 'again':
        return await bot.send_message(cb.from_user.id, 'Напишите своё сообщение:')
    # elif re.match('reply', cb.data):
    #     await state.set_state(User.reader)
    #     await state.update_data(sender_id=get_sender_id(cb.data))
    #     return await bot.send_message(cb.from_user.id, 'Напишите сообщение для ответа:')
