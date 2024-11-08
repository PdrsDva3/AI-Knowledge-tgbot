from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import dp, bot
from db.db_student import get_teacher_list
from db.db_teacher import check_id
import start.keyboard as kb


@dp.callback_query(lambda c: c.data == "start")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    user, i = check_id(callback_query.from_user.id)
    if i == 0:
        kb = [
            [
                InlineKeyboardButton(text="Регистрация", callback_data="teacher"),
            ]]

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        await callback_query.message.edit_text("Здраствуйте, пройдите регистрацию", reply_markup=keyboard)
    else:
        kb = [
            [
                InlineKeyboardButton(text="изменить данные", callback_data="teacher"),
            ],
            [
                InlineKeyboardButton(text="setting", callback_data="setting_teacher"),
            ],
            [
                InlineKeyboardButton(text="new students", callback_data="new_students_teacher"),
            ],
            [
                InlineKeyboardButton(text="my students", callback_data="my_students_teacher"),
            ],
            [
                InlineKeyboardButton(text="help", callback_data="help"),
            ],
            [InlineKeyboardButton(text="return", callback_data="return_to_start")]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        DATA = """
                Здраствуйте,
                Имя        {}
                Уровень       {}
                Сфера      {}
                Описание {}
                """
        await callback_query.message.edit_text(
            DATA.format(user.name, user.grade, user.sphere, user.description),
            reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "return_to_start")
async def cmd_start(callback_query: CallbackQuery):
    kb = [
        [InlineKeyboardButton(text="student", callback_data="info")],
        [InlineKeyboardButton(text="teacher", callback_data="start")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await callback_query.message.edit_text("Здраствуйте", reply_markup=keyboard)


INFO_TEXT = """
Здесь ты можешь увидеть описание своих возможностей как студента.

    Регистрация/изменение данных - заполнить или изменить свою информацию.

    GO! - поиск учителей
    
    Видимость - показывать ли меня учителям

    Список учителей - список всех принятых учителей
"""


@dp.message(Command("start"))
async def cmd_start(message: Message):
    kb = [
        [InlineKeyboardButton(text="student", callback_data="info")],
        [InlineKeyboardButton(text="teacher", callback_data="start")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("Здраствуйте", reply_markup=keyboard)



@dp.callback_query(lambda query: query.data == "info")
async def student_info(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=INFO_TEXT,
        reply_markup=kb.info_and_continue_kb()
    )


@dp.callback_query(lambda query: query.data == "teacher_list")
async def student_info(callback: CallbackQuery):
    list_ = await get_teacher_list(callback.from_user.id)

    TEACHER_LIST = "Список ваших учителей:\n"
    if list_:
        for tch in list_:
            TEACHER_LIST += f"{tch["name"]} - {tch['nickname']}\n"
    else:
        TEACHER_LIST = "У вас пока нет учителей"

    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="info")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=TEACHER_LIST,
        reply_markup=keyboard
    )
