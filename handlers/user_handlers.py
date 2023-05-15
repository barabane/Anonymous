from aiogram import Router, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.deep_linking import create_start_link, decode_payload, encode_payload

from bot_settings import bot
from aiogram.fsm.context import FSMContext
from database.db import db
from states.user import User


router = Router()


@router.message(CommandStart())
async def start_handler(msg: types.Message, command: CommandObject, state: FSMContext):
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
        return await msg.answer('Придумай что хочешь написать:')
    link = await create_start_link(bot, payload=msg.from_user.id, encode=True)
    await msg.answer(f'Твоя ссылка для анонимных сообщений: {link}', disable_web_page_preview=True)


@router.message()
async def msg_handler(msg: types.Message):
    link = await create_start_link(bot, payload=msg.from_user.id, encode=True)
    await msg.answer(f'Твоя ссылка для анонимных сообщений: {link}', disable_web_page_preview=True)


@router.message(User.sender)
async def send_msg_handler(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(data['user_id'], 'У тебя новое сообщение!')
    await bot.send_message(data['user_id'], msg.text)
    await msg.answer(text='Твоё сообщение отправлено!')
    await state.clear()
