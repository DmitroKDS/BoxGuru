from aiogram import types

def create(*buttons: list[tuple[str, str]]) -> types.InlineKeyboardMarkup:

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=text, url=data.split("url:")[1]) if "url:" in data else types.InlineKeyboardButton(text=text, callback_data=data)]
            for text, data in buttons
        ]
    )

    return keyboard