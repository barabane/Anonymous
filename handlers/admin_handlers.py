from aiogram import types
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.admin_kybr import main_keybr
from utils.admin_utils import send_msg_to_all
from states.admin import Admin

from loguru import logger

router = Router()


@router.message(Command('admin'))
async def admin_panel(msg: types.Message):
    await msg.answer('Меню:', reply_markup=main_keybr())


@router.callback_query()
async def cb_handler(cb: types.CallbackQuery, state: FSMContext):
    if cb.data == 'mailing':
        logger.info('mailing')
        await state.set_state(Admin.mailing)
        await cb.answer('Отправь сообщение для рассылки')


@router.message(Admin.mailing)
async def mailing(msg: types.Message):
    await send_msg_to_all(msg)
