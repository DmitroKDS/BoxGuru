from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram import Router

import logging

from bot.functions import question

from config import Config

import bot.handlers.start.start


router = Router()


all_values = [
    "Смартфон 📱", "Ноутбук 💻", "Планшет 🌅"
] + list(Config.translates.get("Смартфон 📱", {}).values()) \
  + list(Config.translates.get("Ноутбук 💻",  {}).values()) \
  + list(Config.translates.get("Планшет 🌅", {}).values())


@router.message(lambda message: message.text in all_values)
async def get(message: types.Message, state: FSMContext) -> None:
    logging.info(f"User select category | User ID and Name: {message.chat.id}, {message.from_user.username}")

    user_id = str(message.chat.id)

    lang = await bot.handlers.start.start.set_lang(user_id, message)
    if lang == None:
        return


    category = message.text

    if category == Config.translates["Смартфон 📱"][lang]:
        await question.ask(message, state, user_id)
    else:
        await message.answer(f"{category} {Config.translates['находится в стадии разработки.'][lang]}")

    await state.clear()