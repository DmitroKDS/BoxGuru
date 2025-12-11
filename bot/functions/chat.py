import asyncio
import telethon
from telethon import TelegramClient, functions, errors
from telethon.tl.types import Channel, Chat, InputChatUploadedPhoto
from config import Config
import traceback
import logging



async def check_conn() -> bool:
    """
    Connects to Telegram via Telethon and checks authorization.
    Returns True if login succeeds, False otherwise.
    """
    client = TelegramClient('bot_session', Config.API_ID, Config.API_HASH)
    await client.connect()

    try:
        if not await client.is_user_authorized():
            await client.send_code_request(Config.YOUR_PHONE)
            code = input("Enter the Telegram login code: ")
            try:
                await client.sign_in(phone=Config.YOUR_PHONE, code=code)
            except telethon.errors.SessionPasswordNeededError:
                pwd = Config.YOUR_TELEGRAM_PASSWORD
                await client.sign_in(password=pwd)

        me = await client.get_me()
        print(f"✅ Connected as {me.first_name} (@{me.username or 'no-username'})")
        return client

    except telethon.errors.PhoneCodeInvalidError:
        print("❌ The code you entered is invalid.")
        return None

    except Exception as e:
        print(f"❌ Unexpected error during connection: {e}")
        return None

    finally:
        await client.disconnect()
    


async def create(user_id: int):
    times = 0
    uid = int(user_id)

    while True:
        try:
            async with Config.client as client:
                # --- 1) Шукаємо вже існуючий чат з цим юзером ---
                # async for d in client.iter_dialogs():
                #     if not d.is_group:
                #         continue

                #     ent = d.entity
                #     try:
                #         if isinstance(ent, Channel):
                #             # суперґрупа / канал
                #             await client(functions.channels.GetParticipantRequest(
                #                 channel=ent,
                #                 participant=uid
                #             ))
                #             return d.id, None  # вже є
                #         elif isinstance(ent, Chat):
                #             # звичайний груповий чат
                #             full = await client(functions.messages.GetFullChatRequest(chat_id=ent.id))
                #             parts = {p.user_id for p in full.full_chat.participants.participants}
                #             if uid in parts:
                #                 return d.id, None  # вже є
                #     except errors.UserNotParticipantError:
                #         pass
                #     except errors.ChatAdminRequiredError:
                #         pass

                # --- 2) Створюємо новий чат ---
                resp = await client(functions.messages.CreateChatRequest(
                    users=[f'@{Config.BOT_USERNAME}', f'@{Config.BOT_ADMIN}'],
                    title='Какой смартфон купить?'
                ))
                chat_id = resp.updates.updates[1].participants.chat_id

                icon = await client.upload_file('icon.jpg')
                await client(functions.messages.EditChatPhotoRequest(
                    chat_id=chat_id,
                    photo=InputChatUploadedPhoto(icon)
                ))

                invite_link = (await client(functions.messages.ExportChatInviteRequest(
                    peer=-chat_id
                ))).link

                await client(functions.messages.EditChatAdminRequest(
                    chat_id=chat_id,
                    user_id=f'@{Config.BOT_USERNAME}',
                    is_admin=True
                ))

                return -chat_id, invite_link

        except Exception:
            times += 1
            if times > 10:
                return None, None
            logging.error("❌ Task failed:\n%s", traceback.format_exc())
            await asyncio.sleep(2)



async def delete(chat_id):
    async with Config.client as client:

        await client(functions.messages.DeleteChatRequest(
            chat_id=chat_id
        ))