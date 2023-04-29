import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

load_dotenv()

bot = Bot(os.environ.get('BOT_TOKEN'))
dp = Dispatcher()
