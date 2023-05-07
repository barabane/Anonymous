from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def inline_kb_build(btns=dict):
    builder = InlineKeyboardBuilder()
    for text, data in btns.items():
        builder.row(types.InlineKeyboardButton(
            text=text, callback_data=data)
        )

    return builder.as_markup()


write_again_kb = inline_kb_build({'ДА!': 'again'})
