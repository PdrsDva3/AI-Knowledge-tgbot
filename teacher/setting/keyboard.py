"""
Этот файл отвечает за создание всех встроенных клавиатур
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def setting_teacher() -> InlineKeyboardMarkup:
    """
    Клавиатура выбора настроек
    :return:
    """
    kb = [
        [
            InlineKeyboardButton(text="show me", callback_data="show_setting_teacher"),
        ],
        [
            InlineKeyboardButton(text="return", callback_data="start"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard



def show_setting_teacher() -> InlineKeyboardMarkup:
    """
    клавиатура выбора показывать ли себя
    :return:
    """
    kb = [
        [
            InlineKeyboardButton(text="Yes", callback_data="show_true_teacher"),
            InlineKeyboardButton(text="No", callback_data="show_false_teacher"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
