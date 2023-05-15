from aiogram import types
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.keyboards import admin_kb
from utils.admin_utils import send_msg_to_admin
from middlewares.middlewares import AdminMiddleware
from states.admin import Admin
from loguru import logger
from database.db import db
from bot_settings import bot

router = Router()

router.message.middleware(AdminMiddleware())


@router.errors()
async def error_handler(error: types.ErrorEvent):
    await send_msg_to_admin(f'Возникла ошибка: {error}')


@router.message(Command('admin'))
async def admin_handler(msg: types.Message):
    await msg.answer('Панель администратора:', reply_markup=admin_kb)


@router.callback_query()
async def cb_handler(cb: types.CallbackQuery, state: FSMContext):
    if cb.data == 'mailing':
        logger.info('mailing')
        await state.set_state(Admin.mailing)
        await cb.answer('Сообщение для рассылки:')


@router.message(Admin.mailing)
async def newsletter(msg: types.Message):
    users = list(db.get_all_users())

    for user in users:
        await bot.send_message(user[0], msg.text)
    await msg.answer('Рассылка завершена!')
