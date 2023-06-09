import asyncio
from bot_settings import bot, dp
from handlers.user_handlers import router as user_router
from handlers.admin_handlers import router as admin_router
from middlewares.middlewares import UsernameMiddleware
from database.db import db
from loguru import logger


async def main():
    dp.include_routers(admin_router, user_router)
    dp.message.middleware(UsernameMiddleware())
    db.init()
    logger.info('start polling...')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
