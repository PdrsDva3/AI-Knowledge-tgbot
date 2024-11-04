"""
Этот файл отвечает за создание всех встроенных клавиатур
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def setting_teacher() -> InlineKeyboardMarkup:
    """
    Клавиатура создания типов сфер деятельности учителя
    :return:
    """
    kb = [
        [
            InlineKeyboardButton(text="range", callback_data="grade_setting_teacher"),
        ],
        [
            InlineKeyboardButton(text="show me", callback_data="show_setting_teacher"),
        ],
        [
            InlineKeyboardButton(text="return", callback_data="start"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def sort_setting_teacher() -> InlineKeyboardMarkup:
    """
    Клавиатура создания типов сфер деятельности учителя
    :return:
    """
    kb = [
        [
            InlineKeyboardButton(text="grade up", callback_data="grade_up_sort_teacher"),
        ],
        [
            InlineKeyboardButton(text="grade down", callback_data="grade_down_sort_teacher"),
        ],
        [
            InlineKeyboardButton(text="sphere", callback_data="sphere_sort_teacher"),
        ],
        [
            InlineKeyboardButton(text="description", callback_data="description_sort_teacher"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def show_setting_teacher() -> InlineKeyboardMarkup:
    """"""
    kb = [
        [
            InlineKeyboardButton(text="Yes", callback_data="show_true_teacher"),
            InlineKeyboardButton(text="No", callback_data="show_false_teacher"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
