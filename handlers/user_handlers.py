from aiogram import Router, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.deep_linking import create_start_link, decode_payload, encode_payload

import re
from loguru import logger
from bot_settings import bot
from utils.user_utils import get_sender_id
from keyboards.user_kybr import write_again_keybr, reply_keybr
from aiogram.fsm.context import FSMContext
from utils.admin_utils import new_user_reg
from database.db import db
from states.user import User


router = Router()


@router.message(CommandStart())
async def start_hand(msg: types.Message, command: CommandObject, state: FSMContext):
    res = db.add_user({
        'id': msg.from_user.id,
        'username': msg.from_user.username,
        'user_url': await create_start_link(bot, payload=msg.from_user.id, encode=True),
    })

    if res['status'] == 'success':
        if not msg.from_user.username:
            await new_user_reg(msg.from_user.id)
        else:
            await new_user_reg(msg.from_user.username)

    user_id = command.args
    if user_id:
        await state.set_state(User.sender)
        await state.update_data(user_id=decode_payload(user_id))
        if user_id == encode_payload(str(msg.from_user.id)):
            return await msg.answer('Упс... Кажется, ты пытаешся написать сообщение самому себе :)')
        return await msg.answer('Отлично! Теперь напиши своё сообщение: ')
    link = await create_start_link(bot, payload=msg.from_user.id, encode=True)
    await msg.answer(f'Твоя ссылка для анонимных сообщений: {link}')


@router.message(User.sender)
async def send_msg(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(data['user_id'], 'У тебя новое сообщение!')
    await bot.send_message(data['user_id'], msg.text)
    await msg.delete()
    await msg.answer(text='Твоё сообщение отправлено!')
    # await msg.answer(text='Хочешь написать еще что-нибудь?', reply_markup=write_again_keybr())
    await state.clear()


@router.message(User.reader)
async def send_reply(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(data['sender_id'], 'Сообщение отправлено!')


@router.callback_query()
async def cb_handler(cb: types.CallbackQuery, state: FSMContext):
    if cb.data == 'again':
        await cb.answer()
        await bot.send_message(cb.from_user.id, 'Напишите своё сообщение:')
    # elif re.match('reply', cb.data):
    #     await state.set_state(User.reader)
    #     await state.update_data(sender_id=get_sender_id(cb.data))
    #     return await bot.send_message(cb.from_user.id, 'Напишите сообщение для ответа:')
