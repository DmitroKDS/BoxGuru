from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router

import logging

from config import Config

from bot.functions import question as fs_question

from googletrans import Translator

import bot.handlers.start.start


router = Router()

class your_answer(StatesGroup):
    waiting = State()


@router.callback_query(F.data.contains("answ"))
async def get(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    logging.info(f"User select an answer | User ID and Name: {callback_query.message.chat.id}, {callback_query.message.from_user.username}")

    await state.clear()

    user_id = str(callback_query.message.chat.id)

    lang = await bot.handlers.start.start.set_lang(user_id, callback_query.message)
    if lang == None:
        return




    question = len(Config.answers.get(user_id, []))
    option = int(callback_query.data.split("_")[1])

    answ = Config.questions[lang][question]["options"][option]

    if Config.questions["ru"][question]["options"][option]=="Свой вариант ответа":
        await state.update_data(delete_inline = callback_query.message.delete_reply_markup())
        
        await state.set_state(your_answer.waiting)

        await callback_query.message.answer(
Config.translates["Напиши свой вариант ответа:"][lang]
        )
    else:
        Config.answers.setdefault(user_id, []).append(Config.questions["ru"][question]["options"][option])

        await callback_query.message.delete_reply_markup()

        await callback_query.message.answer(
f"""{Config.translates["Ты выбрал:"][lang]} {answ}"""
        )

        await fs_question.ask(callback_query.message, state, user_id)



@router.message(your_answer.waiting)
async def wrote_answer(message: types.Message, state: FSMContext):
    logging.info(f"User wrote own answer | User ID and Name: {message.chat.id}, {message.from_user.username}")

    user_id = str(message.chat.id)

    lang = await bot.handlers.start.start.set_lang(user_id, message)
    if lang == None:
        return
    
    
    await (await state.get_data())["delete_inline"]

    answ = message.text
    
    await state.clear()

    async with Translator() as translator:
        answ = (await translator.translate(answ, dest='ru')).text
    
    Config.answers.setdefault(user_id, []).append(answ)

    await fs_question.ask(message, state, user_id)