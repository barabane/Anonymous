import asyncio
from bot_settings import bot, dp
from handlers.user_handlers import router


async def main():
    dp.include_routers(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
