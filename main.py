import asyncio
import logging
import random

from aiogram import Bot, Dispatcher, types
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.formatting import Bold, Text, as_list

from config import API_KEY, dp, bot
from db_requests import get_all, update_all, insert_all, get_all_teachers
import student.search.search
import student.search.keyboard
import student.registration.keyboard
import student.registration.registration


# todo
# ========================================================================================================= keyboards
def starting_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="student", callback_data="info")],
        [InlineKeyboardButton(text="teacher", callback_data="teacher")],
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


def return_go_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="cmd_go")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def cmd_filters_kb() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Выбрать уровень", callback_data="gradef")],
        [types.InlineKeyboardButton(text="Выбрать сферу", callback_data="spheref")],
        [types.InlineKeyboardButton(text="Применить и перейти", callback_data="fsearch")],
        [types.InlineKeyboardButton(text="Назад", callback_data="cmd_go")]

    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# todo
# ======================================================================================================


@dp.message(Command("start"))
async def cmd_start(message: Message):
    content = as_list(
        Text(
            "Hello, ",
            Bold(message.from_user.first_name),
            ". Это бот для поиска менторов и менти."
            " Пожалуйста выбери свой роль. Студент - ..., а Учитель - ... "

        )
    )
    await message.answer(
        **content.as_kwargs(),
        reply_markup=starting_kb()
    )


INFO_TEXT = """
Здесь ты можешь увидеть описание своих возможностей как студента.
        
    Регистрация/изменение данных - заполнить или изменить свою информацию.
    
    GO! - поиск учителей
    
    Список учителей - список всех принятых учителей
"""


@dp.callback_query(lambda query: query.data == "info")
async def student_info(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=INFO_TEXT,
        reply_markup=info_and_continue_kb()
    )


logging.basicConfig(level=logging.DEBUG)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

# 1)
# todo сделать поиск с учетом фильтров

# 2)
# todo раскинуть всё по папкам
# todo реализовать отправление-принятие заявки
# todo
# реализовать список учителей
