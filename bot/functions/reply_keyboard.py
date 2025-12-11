from aiogram import types

def create(*buttons: list[str]) -> types.ReplyKeyboardMarkup:
    keyboard = []
    for button in buttons:
        keyboard.append([types.KeyboardButton(text=button)])

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=keyboard
    )

    return keyboard

def create_with_row(*buttons: list[tuple[str, str]]) -> types.ReplyKeyboardMarkup:
    keyboard = [
        [
            types.KeyboardButton(text=button)
            for button in row
        ]
        for row in buttons
    ]
    
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=keyboard
    )

    return keyboard