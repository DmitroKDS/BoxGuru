from aiogram.filters import CommandStart
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram import Router

import logging

from config import Config

from bot.functions import reply_keyboard, inline_keyboard



router = Router()


@router.message(CommandStart())
async def init(message: types.Message, state: FSMContext) -> None:
    logging.info(f"Start | User ID and Name: {message.chat.id}, {message.chat.username}")


    user_id = str(message.chat.id)
    lang = await set_lang(user_id, message)

    if user_id in Config.user_lang:
        await message.answer(
            Config.translates["Выберите категорию:"][lang],
            reply_markup=reply_keyboard.create_with_row((Config.translates["Смартфон 📱"][lang], Config.translates["Ноутбук 💻"][lang]), (Config.translates["Планшет 🌅"][lang], "Language 🌍"), ("Админка",)) if message.chat.username in Config.admins else reply_keyboard.create_with_row((Config.translates["Смартфон 📱"][lang], Config.translates["Ноутбук 💻"][lang]), (Config.translates["Планшет 🌅"][lang], "Language 🌍"))
        )
    


async def set_lang(user_id, message: types.Message):
    if user_id not in Config.user_lang or Config.user_lang[user_id]==None:
        Config.pay_lang[user_id] = message.from_user.language_code
        await message.answer("HI", reply_markup=reply_keyboard.create("Админка") if message.chat.username in Config.admins else None)

        await message.answer(
            f"""Let's choose language to speak:""",
            reply_markup=inline_keyboard.create(
                *[
                    (lang, f'lang_{code}')
                    for code, lang in Config.languages.items()
                ]
            )
        )

        return "ru"



    return Config.user_lang[user_id]



@router.callback_query(F.data.contains("lang_"))
async def lang_set(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = str(callback_query.message.chat.id)

    Config.user_lang[user_id] = callback_query.data.split("lang_")[1]
    if user_id in Config.answers: 
        Config.answers.pop(user_id)
    lang = Config.user_lang.get(user_id, "ru")

    await callback_query.message.answer(
        Config.translates["Выберите категорию:"][lang],
        reply_markup=reply_keyboard.create_with_row((Config.translates["Смартфон 📱"][lang], Config.translates["Ноутбук 💻"][lang]), (Config.translates["Планшет 🌅"][lang], "Language 🌍"), ("Админка",)) if callback_query.message.chat.username in Config.admins else reply_keyboard.create_with_row((Config.translates["Смартфон 📱"][lang], Config.translates["Ноутбук 💻"][lang]), (Config.translates["Планшет 🌅"][lang], "Language 🌍"))
    )



@router.message(lambda message: message.text == "Language 🌍")
async def get(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        f"""Let's choose language to speak:""",
        reply_markup=inline_keyboard.create(
            *[
                (lang, f'lang_{code}')
                for code, lang in Config.languages.items()
            ]
        )
    )