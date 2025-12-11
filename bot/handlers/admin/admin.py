from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router

import logging

import io

from bot.functions import inline_keyboard

from config import Config

from bot.functions import question as fs_question

import bot.handlers.start.start


router = Router()

class questions(StatesGroup):
    waiting = State()

class admin(StatesGroup):
    waiting = State()

class langs(StatesGroup):
    waiting = State()

class prices(StatesGroup):
    waiting = State()


@router.message(lambda message: message.text == 'Админка')
async def init(message: types.Message, state: FSMContext):
    user_id = str(message.chat.id)

    lang = await bot.handlers.start.start.set_lang(user_id, message)
    if lang == None:
        return


    if message.from_user.username not in Config.admins:
        await message.answer(
Config.translates["У вас нет прав"][lang]
        )
        
        return
    
    await message.answer(
"""Вы в админке""",
        reply_markup=inline_keyboard.create(('Загрузить языки', 'load_langs'), ('Загрузить вопроси', 'load_questions'), ('Загрузить прайсы', 'load_prices'), ('Добавить админа', 'add_admin'))
    )

    await state.clear()


@router.callback_query(F.data == "load_questions")
async def load_questions(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    message = callback_query.message

    await message.answer(
"""Пожалуйста, загрузите файл с вопросами в формате xlsx"""
    )

    await state.clear()

    await state.set_state(questions.waiting)


@router.message(F.content_type.in_(['document']), questions.waiting)
async def uploaded_questions(message: types.Message, state: FSMContext):
    downloaded = io.BytesIO()
    
    await message.bot.download(message.document, destination=downloaded)

    try:
        Config.questions = await fs_question.upload(downloaded)
        Config.answers = {}

        await message.answer(
f"""Вопросы успешно загружены и добавлены.""",
        )
    except Exception as e:
        await message.answer(
f"""Произошла ошибка при обработке файла: {str(e)}""",
        )

    await state.clear()




@router.callback_query(F.data == "load_langs")
async def load_langs(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    message = callback_query.message

    await message.answer(
"""Пожалуйста, загрузите файл с языкаме в формате xlsx"""
    )

    await state.clear()

    await state.set_state(langs.waiting)


@router.message(F.content_type.in_(['document']), langs.waiting)
async def uploaded_langs(message: types.Message, state: FSMContext):
    downloaded = io.BytesIO()
    
    await message.bot.download(message.document, destination=downloaded)

    try:
        Config.languages, Config.translates = await fs_question.upload_langs(downloaded)

        await message.answer(
f"""Языки загружены и добавлены.""",
        )
    except Exception as e:
        await message.answer(
f"""Произошла ошибка при обработке файла: {str(e)}""",
        )

    await state.clear()





@router.callback_query(F.data == "load_prices")
async def load_prices(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    message = callback_query.message

    await message.answer(
"""Пожалуйста, загрузите файл с вопросами в формате xlsx"""
    )

    await state.clear()

    await state.set_state(prices.waiting)


@router.message(F.content_type.in_(['document']), prices.waiting)
async def uploaded_prices(message: types.Message, state: FSMContext):
    downloaded = io.BytesIO()
    
    await message.bot.download(message.document, destination=downloaded)

    try:
        Config.prices = await fs_question.upload_prices(downloaded)

        await message.answer(
f"""Прайсы успешно загружены и добавлены.""",
        )
    except Exception as e:
        await message.answer(
f"""Произошла ошибка при обработке файла: {str(e)}""",
        )

    await state.clear()







@router.callback_query(F.data == "add_admin")
async def add_admin(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    message = callback_query.message

    await message.answer(
"""Напишите nickname нового администратора:"""
    )

    await state.clear()

    await state.set_state(admin.waiting)


@router.message(admin.waiting)
async def uploaded_admin(message: types.Message, state: FSMContext):
    admin_nickname = message.text

    Config.admins.append(admin_nickname)
    
    await message.answer(
f"""Админ {admin_nickname} добавлен."""
    )

    await state.clear()