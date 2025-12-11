from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, Bot

from bot.functions import inline_keyboard

from bot.functions import chat

from bot.handlers.start import start

import logging

from config import Config

from googletrans import Translator

import bot.handlers.start.start



router = Router()


async def payment_test(message: types.Message, state: FSMContext):
    user_id = str(message.chat.id)

    lang = await bot.handlers.start.start.set_lang(user_id, message)
    if lang == None:
        return

    chat_id, invite_link = await chat.create()
    
    answers = "\n\n".join(
        f"{Config.questions['ru'][i]['text']}:\n<b>{answer}</b>"
        for i, answer in Config.answers.get(user_id, [])
    )

    await message.bot.send_message(
        chat_id,
f"""{Config.translates["Привет."][lang]}
{Config.translates["Тут все твои ответы:"][lang]}
{answers}.""", 
        disable_web_page_preview=True
    )

    await message.answer(
f"""{Config.translates["Весь разговор будет продолжаться в этом чате"][lang]}

{invite_link}""",
        reply_markup=inline_keyboard.create((Config.translates['Пройти опрос еще раз'][lang], 'again'))
    )

    Config.pays[user_id] = 0

    await state.clear()



@router.pre_checkout_query()
async def checkout(query: types.PreCheckoutQuery, state: FSMContext) -> None:
    await state.clear()

    user_id = query.from_user.id
    lang = Config.user_lang.get(user_id, "ru")

    await query.answer(
        ok=True,
        error_message=Config.translates["Инопланетяне попытались украсть CVV вашей карты, но мы успешно защитили ваши данные."][lang]
            + Config.translates["Попробуйте оплатить снова через несколько минут, нам нужно немного отдохнуть."][lang]
    )



@router.message(F.successful_payment)
async def successful(message: types.Message, state: FSMContext):
    logging.info(f"User made a payment | User ID and Name: {message.chat.id}, {message.from_user.username}")

    invoice_payload = message.successful_payment.invoice_payload
    print(message.successful_payment)

    user_id = str(message.chat.id)

    lang = await bot.handlers.start.start.set_lang(user_id, message)
    if lang == None:
        return

    if "chat" in invoice_payload:
        chat_id = int(invoice_payload.split("_")[1])
        question, invoice_id = Config.pre_questions.get(invoice_payload.replace("chat_", ""), None)
        try:
            await message.bot.delete_message(chat_id=chat_id, message_id=int(invoice_id))
        except:
            pass
        if question == None:
            Config.pays.setdefault(user_id, 0) 
            Config.pays[user_id] += 1

            await message.bot.send_message(
                chat_id,
                Config.translates["Теперь ты можешь написать вопрос и мы в ближайшое время тебе ответим"][lang]
            )
        else:
            try:
                await message.bot.delete_message(chat_id=chat_id, message_id=int(invoice_payload.split("_")[2]))
            except:
                pass

            # async with Translator() as translator:
            #     is_ru = (await translator.detect(question)).lang == 'ru'
            Config.pays[user_id] -= 1


            await message.bot.send_message(
                chat_id,
f"""{Config.translates["Ты задал вопрос:"][lang]}
<b>{question}</b>"""
            )

    else:
        chat_id, invite_link = await chat.create(user_id)
        
        answers = "\n\n".join(
            f"{Config.questions['ru'][i]['text']}:\n<b>{answer}</b>"
            for i, answer in enumerate(Config.answers.get(user_id, []))
        )

        await message.bot.send_message(
            chat_id,
f"""{Config.translates["Привет."][lang]}
{Config.translates["Тут все твои ответы:"][lang]}
{answers}.""", 
            disable_web_page_preview=True,
            reply_markup=types.ReplyKeyboardRemove()
        )


        await message.answer(
f"""<b style="red">{Config.translates["Ответ будет в этом чате, поэтому смело нажимайте на ссылку — она защищена и безопасна 🔒"][lang]}</b>"""
        )

        await message.answer(
f"""{Config.translates["Весь разговор будет продолжаться в этом чате"][lang]}

{invite_link}""",
            reply_markup=inline_keyboard.create((Config.translates['Пройти опрос еще раз'][lang], 'again'))
        )

        Config.pays.setdefault(user_id, 0)

    await state.clear()


@router.callback_query(F.data.contains("again"))
async def again(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete_reply_markup()

    user_id = str(callback_query.message.chat.id)

    Config.answers.pop(user_id)

    await state.clear()

    await start.init(callback_query.message, state)