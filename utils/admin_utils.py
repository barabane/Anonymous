import os
from loguru import logger
from aiogram import types
from bot_settings import bot
from database.db import db


async def new_user_reg(username: str):
    await bot.send_message(os.environ.get('ADMIN_ID'), f'@{username} зарегистрировался в боте')


async def send_msg_to_all(msg: types.Message):
    users = list(db.get_all_users())
    logger.info(users)

    for user in users:
        await bot.send_message(user[0], msg.text)
    await msg.answer('Рассылка заверщена!')
