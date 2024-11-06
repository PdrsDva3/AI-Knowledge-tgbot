from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def registration_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Имя", callback_data="name")],
        [InlineKeyboardButton(text="Уровень", callback_data="grade")],
        [InlineKeyboardButton(text="Сфера", callback_data="sphere")],
        [InlineKeyboardButton(text="Краткий рассказ", callback_data="bio")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def registration_okay_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Имя", callback_data="name")],
        [InlineKeyboardButton(text="Уровень", callback_data="grade")],
        [InlineKeyboardButton(text="Сфера", callback_data="sphere")],
        [InlineKeyboardButton(text="Краткий рассказ", callback_data="bio")],
        [InlineKeyboardButton(text="Всё верно", callback_data="all_is_okay")],
        [InlineKeyboardButton(text="Назад (нажимая после изменений, они не сохранятся)", callback_data="info")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# NLP, CV,RecSys, Audio, Classic ML, любой
def choose_sphere_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="NLP", callback_data="NLP_sphere")],
        [InlineKeyboardButton(text="CV", callback_data="CV_sphere")],
        [InlineKeyboardButton(text="RecSys", callback_data="RecSys_sphere")],
        [InlineKeyboardButton(text="Audio", callback_data="Audio_sphere")],
        [InlineKeyboardButton(text="Classic ML", callback_data="Classic_ML_sphere")],
        [InlineKeyboardButton(text="Любой", callback_data="Any_sphere")],
        [InlineKeyboardButton(text="Назад", callback_data="return")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# no_work, intern, junior, middle. senior
def choose_grade_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="No work", callback_data="no_work_grade")],
        [InlineKeyboardButton(text="Intern", callback_data="intern_grade")],
        [InlineKeyboardButton(text="Junior", callback_data="junior_grade")],
        [InlineKeyboardButton(text="Middle", callback_data="middle_grade")],
        [InlineKeyboardButton(text="Senior", callback_data="senior_grade")],
        [InlineKeyboardButton(text="Назад", callback_data="return")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def return_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="return")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def info_and_continue_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Регистрация", callback_data="registration")],
        [InlineKeyboardButton(text="GO!", callback_data="cmd_go")],
        [InlineKeyboardButton(text="Список учителей", callback_data="teacher_list")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
