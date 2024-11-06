"""Реализация регистрации"""
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup

import db.db
import teacher.model
from db.db import check_id, add_user

import teacher.setting.keyboard as kb
# from main import dp
from config import TOKEN_TG, dp, bot, router


# /settings_teacher
# 1) Настройка: по чему ранжировать
# 1.1) По грейду
# 1.2) По сфере
# 1.3) По близости описания человека (сделаем мы)
# 2) Показывать ли свою анкету в поиске: True/False

class RegistrateTeacher(StatesGroup):
    sort = State()
    show = State()
    wait = State()

SORT = {
    "grade_up": 1,
    "grade_down": 2,
    "sphere": 3,
    "description": 4
}

SHOW_SORT = {
    1: "grade up",
    2: "grade down",
    3: "sphere",
    4: "description"
}

DATA = """
Ваши настройки
sort {}
show me {}
"""


async def do_text(state: FSMContext):
    user_data = await state.get_data()
    show = user_data["show"]
    sort = user_data["sort"]
    call = user_data['call']
    db.db.change_show(call.from_user.id, show)
    db.db.change_sort(call.from_user.id, sort)
    await call.message.edit_text(DATA.format( SHOW_SORT[sort], show),
                                 reply_markup=kb.setting_teacher())


@dp.callback_query(lambda c: c.data == "setting_teacher")
async def start_registration(call: CallbackQuery, state: FSMContext):
    user, i = check_id(call.from_user.id)
    await state.update_data(sort=user.sort, show=user.show, call=call)
    await do_text(state)


@dp.callback_query(lambda c: c.data == "grade_setting_teacher")
async def start_registration(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите ваше имя", reply_markup=kb.sort_setting_teacher())
    await state.set_state(RegistrateTeacher.sort)


@dp.callback_query(lambda c: c.data == "show_setting_teacher")
async def start_registration(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите ваше имя", reply_markup=kb.show_setting_teacher())
    await state.set_state(RegistrateTeacher.show)

@dp.callback_query(lambda c: (c.data.split("_")[0] == "show" and c.data.split("_")[2] == "teacher"))
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data.split("_")[1] == "true":
        await state.update_data(show=True)
    elif callback_query.data.split("_")[1] == "false":
        await state.update_data(show=False)
    await do_text(state)
    await state.set_state(RegistrateTeacher.wait)


@dp.callback_query(lambda c: (c.data.split("_")[-2:] == ["sort", "teacher"]))
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(sort=SORT["_".join(callback_query.data.split("_")[:-2])])
    await do_text(state)
    await state.set_state(RegistrateTeacher.wait)
