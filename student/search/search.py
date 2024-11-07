import random

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from db.db_student import get_all_teachers, get_teacher_by_id
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
    # бесполезные строки, но могут помочь при развитии функционала (state чистится в cmd_go)
    # teacher_data = await state.get_data()
    # if "list" not in teacher_data:
    random_list = await get_random_teachers()
    await state.update_data(list=random_list, index=0)
    await print_teacher(callback, state)


@dp.callback_query(lambda c: c.data == "next_teacher")
async def searching_next(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data.get("index", 0) + 1

    await state.update_data(index=index)
    await print_teacher(callback, state)


@dp.callback_query(lambda c: c.data == "agree")
async def agree_request(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    list_ = data["list"]
    index_ = data["index"]
    user_id = list_[index_]["id"]
    buttons = [
        [InlineKeyboardButton(text="Принять", callback_data=f"{callback.from_user.id}_accept")],
        [InlineKeyboardButton(text="Отказать", callback_data=f"{callback.from_user.id}_deny")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(user_id, "пришла новая заявка", reply_markup=keyboard)

RESPONSE_TEACHER_DATA="""
Ваша заявка для
Имя:       {}
Уровень:   {}
Сфера:     {}
Краткий рассказ:
{}

была ОТКЛОНЕНА
"""

@dp.callback_query(lambda c: c.data.split("_")[-1] == "deny")
async def deny_request(callback: CallbackQuery):
    buttons = [
        [InlineKeyboardButton(text="Принять", callback_data="ok")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    teacher_id = callback.from_user.id
    teacher_info = (await get_teacher_by_id(teacher_id))[0]
    await bot.send_message(int(callback.data.split("_")[0]), RESPONSE_TEACHER_DATA.format(teacher_info["name"], teacher_info["grade"],
                                                                    teacher_info["sphere"], teacher_info["bio"]),
                           reply_markup=keyboard)
    await callback.message.delete()

@dp.callback_query(lambda c: c.data == "ok")
async def deny_request(callback: CallbackQuery):
    await callback.message.delete()