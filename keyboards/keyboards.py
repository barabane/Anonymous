from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_inline_kb(btns=dict):
    builder = InlineKeyboardBuilder()
    for text, data in btns.items():
        builder.row(types.InlineKeyboardButton(
            text=text, callback_data=data)
        )

    return builder.as_markup()


write_again_kb = build_inline_kb({'Написать': 'write_again'})
admin_kb = build_inline_kb({'Рассылка': 'mailing'})
