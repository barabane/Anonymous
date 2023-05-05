from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_keybr():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Рассылка", callback_data='mailing')
    )

    return builder.as_markup()
