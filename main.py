import asyncio

from aiogram import Dispatcher

from bot.handlers.start import router as start_router
from bot.handlers.admin import router as admin_router
from bot.handlers.answer import router as answer_router
from bot.handlers.category import router as category_router

from bot.handlers.errors import catch

import logging
from logging.handlers import RotatingFileHandler

from config import Config

from bot.functions import chat

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

import os

import updater



def register_routes(dispatcher: Dispatcher) -> None:
    """
    Initialize routes of the bot
    """
    logging.info(f"Initialize routers")

    dispatcher.include_router(start_router)
    dispatcher.include_router(admin_router)
    dispatcher.include_router(answer_router)
    dispatcher.include_router(category_router)


async def run_bot():
    """
    The main function that create and start bot
    """

    dispatcher = Dispatcher()

    dispatcher.errors.register(catch)

    register_routes(dispatcher)


    bot = Bot(
        token=Config.BOT_TOKEN_API,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )


    await dispatcher.start_polling(bot, timeout=160)



async def main():
    Config.client = await chat.check_conn()

    await asyncio.gather(
        run_bot(),
        updater.init()
    )




if __name__ == '__main__':
    # Start loggining
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    fh = RotatingFileHandler(
        filename="bot.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)

    root.addHandler(fh)
    root.addHandler(ch)


    # Run the bot
    folders = ["cache"]
    for f in folders:
        if not os.path.exists(f):
            os.makedirs(f)

    asyncio.run(main())