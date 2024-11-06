import random

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from db_requests import get_all_teachers
from config import bot, dp
from student.search import keyboard as kb


@dp.callback_query(lambda c: c.data == "cmd_go")
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


async def get_random_teachers() -> list[dict]:
    list_ = await get_all_teachers()
    random.shuffle(list_)
    return list_


TEACHER_DATA = """
Имя:    {}
Уровень:    {}
Сфера:    {}
Краткий рассказ:
{}
"""


class Searching(StatesGroup):
    search = State()


async def print_teacher(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    teacher_list = data.get("list", [])
    index = data.get("index", 0)

    if index < len(teacher_list):
        teacher = teacher_list[index]
        await callback.message.edit_text(
            text=TEACHER_DATA.format(teacher["name"], teacher["grade"], teacher["sphere"], teacher["bio"]),
            reply_markup=kb.searching_kb()
        )
    else:
        await callback.message.edit_text(
            text="Учителя закончились((",
            reply_markup=kb.return_go_kb()
        )


@dp.callback_query(lambda c: c.data == "search")
async def searching(callback: CallbackQuery, state: FSMContext):
    teacher_data = await state.get_data()
    if "list" not in teacher_data:
        random_list = await get_random_teachers()
        await state.update_data(list=random_list, index=0)
        await print_teacher(callback, state)


@dp.callback_query(lambda c: c.data == "next_teacher")
async def searching_next(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data.get("index", 0) + 1

    await state.update_data(index=index)
    await print_teacher(callback, state)
