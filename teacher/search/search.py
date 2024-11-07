import random

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from config import bot, dp
from db.db_teacher import get_all_student
from teacher.search import keyboard as kb


@dp.callback_query(lambda c: c.data == "new_students_teacher")
async def cmd_go(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="""
            Ты можешь выставить определенные фильтры \nили искать по всем подряд
            """,
        reply_markup=kb.search_or_filters_kb()
    )


async def get_random_student() -> list[dict]:
    list_ = await get_all_student()
    random.shuffle(list_)
    return list_


TEACHER_DATA = """
Имя:    {}
Уровень:    {}
Сфера:    {}
Краткий рассказ:
{}
"""


async def print_search(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    students_list = data.get("list", [])
    index = data.get("index", 0)

    if index < len(students_list):
        teacher = students_list[index]
        await callback.message.edit_text(
            text=TEACHER_DATA.format(teacher["name"], teacher["grade"], teacher["sphere"], teacher["bio"]),
            reply_markup=kb.searching_kb()
        )
    else:
        await callback.message.edit_text(
            text="студенты закончились((",
            reply_markup=kb.return_go_kb()
        )


@dp.callback_query(lambda c: c.data == "search_students")
async def searching(callback: CallbackQuery, state: FSMContext):
    # бесполезные строки, но могут помочь при развитии функционала (state чистится в cmd_go)
    # teacher_data = await state.get_data()
    # if "list" not in teacher_data:
    random_list = await get_random_student()
    await state.update_data(list=random_list, index=0)
    await print_search(callback, state)


@dp.callback_query(lambda c: c.data == "next_student")
async def searching_next(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data.get("index", 0) + 1

    await state.update_data(index=index)
    await print_search(callback, state)
