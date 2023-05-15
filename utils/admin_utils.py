import os
from loguru import logger
from aiogram import types
from bot_settings import bot
from database.db import db


async def send_msg_to_admin(msg):
    await bot.send_message(os.environ.get('ADMIN_ID'), msg)
