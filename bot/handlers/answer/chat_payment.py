from aiogram import types, F, filters
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router

import logging

from config import Config

from bot.functions import inline_keyboard

from googletrans import Translator

import bot.handlers.start.start


router = Router()


@router.chat_member(filters.ChatMemberUpdatedFilter(filters.IS_NOT_MEMBER >> filters.IS_MEMBER))
async def welcome_new_member(update: types.ChatMemberUpdated, state: FSMContext) -> None:
    user_id  = str(update.new_chat_member.user.id)
    lang = Config.user_lang.get(user_id, "ru")
    
    await update.answer(
        Config.translates["Ожидайте в течении 24 часов тебе ответят."][lang]
    )
    
    await state.clear()




@router.message(F.chat.type == "group")
async def delete_chat_messages(message: types.Message):
    user_id = str(message.from_user.id)

    lang = Config.user_lang.get(user_id, "ru")

    if message.from_user.username not in Config.admins and message.from_user.username!=Config.BOT_ADMIN:
        pays = Config.pays.get(user_id, 0)
        question = message.text
        try:
            await message.delete()
        except:
            pass

        if pays > 0 and question!=None:
            # async with Translator() as translator:
            #     is_ru = (await translator.detect(question)).lang == 'ru'
            Config.pays[user_id] -= 1


            await message.answer(
    f"""{Config.translates["Ты задал вопрос:"][lang]}
<b>{question}</b>"""
            )
#             else:
#                 async with Translator() as translator:
#                     translate = (await translator.translate(question, dest='ru')).text

#                 await message.answer(
#     f"""{Config.translates["Ты задал вопрос:"][lang]}
# <b>{question}</b>
# Перевод
# <b>{translate}</b>"""
#                 )
        elif question != None:
            message = await message.answer(
f"""{Config.translates['Твое сообщение:'][lang]}
<b>{question}</b>
{Config.translates['еще не было отправлено. Для отправки нажмите "Оплатить"'][lang]}"""
            )
            
            key = f"{message.chat.id}_{message.message_id}"
            message = await message.answer_invoice(
                title=Config.translates['Оплати для отпраки сообщения'][lang],
                description="👇",
                payload=f"chat_{key}",
                prices=[
                    types.LabeledPrice(label="XTR", amount=Config.prices.get(Config.pay_lang.get(user_id, "undefined"))),
                ],
                currency="XTR"
            )
            Config.pre_questions[key] = [question, message.message_id]