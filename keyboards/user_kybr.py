from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def write_again_keybr():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="ДА!", callback_data='again')
    )

    return builder.as_markup()


def reply_keybr(sender_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Написать ответ", callback_data=f'reply_{sender_id}')
    )

    return builder.as_markup()
