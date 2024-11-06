"""
Этот файл отвечает за создание всех встроенных клавиатур
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def sphere_teacher() -> InlineKeyboardMarkup:
    """
    Клавиатура создания типов сфер деятельности учителя
    :return:
    """
    kb = [
        [
            InlineKeyboardButton(text="NLP", callback_data="NLP_sphere_teacher"),
        ],
        [
            InlineKeyboardButton(text="CV", callback_data="CV_sphere_teacher"),
        ],
        [
            InlineKeyboardButton(text="RecSys", callback_data="RecSys_sphere_teacher"),
        ],
        [
            InlineKeyboardButton(text="Audio", callback_data="Audio_sphere_teacher"),
        ],
        [
            InlineKeyboardButton(text="Classic ML", callback_data="Classic_ML_sphere_teacher"),
        ],
        [
            InlineKeyboardButton(text="Any", callback_data="Any_sphere_teacher"),
        ],
        [
            InlineKeyboardButton(text="return", callback_data="return_reg_teacher"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def grade_teacher() -> InlineKeyboardMarkup:
    """
    Клавиатура создания уровня работы
    :return:
    """
    kb = [
        [
            InlineKeyboardButton(text="no work", callback_data="no_work_grade_teacher")
        ],
        [
            InlineKeyboardButton(text="intern", callback_data="intern_grade_teacher")
        ],
        [
            InlineKeyboardButton(text="junior", callback_data="junior_grade_teacher")
        ],
        [
            InlineKeyboardButton(text="middle", callback_data="middle_grade_teacher")
        ],
        [
            InlineKeyboardButton(text="senior", callback_data="senior_grade_teacher")
        ],
        [
            InlineKeyboardButton(text="return", callback_data="return_reg_teacher"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def reg_teacher() -> InlineKeyboardMarkup:
    """
    Базовая клавиатура выбора пункта для регистрации
    :return:
    """
    kb = [
        [
            InlineKeyboardButton(text="Имя", callback_data="name_teacher")
        ],
        [
            InlineKeyboardButton(text="Отчество", callback_data="surname_teacher")
        ],
        [
            InlineKeyboardButton(text="Уровень", callback_data="grade_teacher")
        ],
        [
            InlineKeyboardButton(text="Сфера", callback_data="sphere_teacher")
        ],
        [
            InlineKeyboardButton(text="Краткий рассказ", callback_data="description_teacher"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def reg_teacher_okay() -> InlineKeyboardMarkup:
    """
    Конечная клавиатура выбора пункта для регистрации
    :return:
    """
    kb = [
        [
            InlineKeyboardButton(text="name", callback_data="name_teacher")
        ],
        [
            InlineKeyboardButton(text="surname", callback_data="surname_teacher")
        ],
        [
            InlineKeyboardButton(text="grade", callback_data="grade_teacher")
        ],
        [
            InlineKeyboardButton(text="sphere", callback_data="sphere_teacher")
        ],
        [
            InlineKeyboardButton(text="description", callback_data="description_teacher"),
        ],
        [
            InlineKeyboardButton(text='Все верно', callback_data="reg_teacher_ok"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def reg_return_teacher() -> InlineKeyboardMarkup:
    """
    Клавиатура для возвращения на регистрацию
    :return:
    """
    kb = [
        [
            InlineKeyboardButton(text="return", callback_data="return_reg_teacher"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
