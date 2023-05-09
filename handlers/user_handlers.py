from aiogram import Router, types
from aiogram.filters import CommandStart, CommandObject, Text
from aiogram.utils.deep_linking import create_start_link, decode_payload, encode_payload

import re
from loguru import logger
from bot_settings import bot
from utils.user_utils import get_sender_id
from keyboards.keyboards import write_again_kb
from aiogram.fsm.context import FSMContext
from database.db import db
from states.user import User
from pprint import pprint


router = Router()


@router.errors()
async def error_handler(error: types.ErrorEvent):
    await send_msg_to_admin(f'Возникла ошибка: {error}')


@router.message(CommandStart())
async def start_hand(msg: types.Message, command: CommandObject, state: FSMContext):
    await db.reg_user({
        'id': msg.from_user.id,
        'username': msg.from_user.username,
        'user_url': await create_start_link(bot, payload=msg.from_user.id, encode=True),
    })

    user_id = command.args
    if user_id:
        if user_id == encode_payload(str(msg.from_user.id)):
            return await msg.answer('Упс... Кажется, ты пытаешся написать сообщение самому себе :)')

        await state.set_state(User.sender)
        await state.update_data(user_id=decode_payload(user_id))
        return await msg.answer('Напиши своё сообщение:')
    link = await create_start_link(bot, payload=msg.from_user.id, encode=True)
    await msg.answer(f'Твоя ссылка для анонимных сообщений: {link}')


@router.message(User.sender)
async def send_msg(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(data['user_id'], 'У тебя новое сообщение!')
    await bot.send_message(data['user_id'], msg.text)
    await msg.answer(text='Твоё сообщение отправлено!')
    await state.clear()
    # await msg.answer(text='Хочешь написать еще что-нибудь?', reply_markup=write_again_kb)


# @router.callback_query(Text('write_again'))
# async def cb_handler(cb: types.CallbackQuery, state: FSMContext):
#     logger.info(cb)
#     if cb.data == 'write_again':
#         await state.set_state(User.sender)
#         await cb.answer('.')
#         await bot.send_message(cb.from_user.id, 'Напишите своё сообщение:')
