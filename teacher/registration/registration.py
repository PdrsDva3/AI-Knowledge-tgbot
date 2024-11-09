"""Реализация регистрации"""
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup

import teacher.model
import teacher.registration.keyboard as kb
from config import dp, NoneData
from db.db_teacher import check_id, add_user


class RegistrateTeacher(StatesGroup):
    name = State()
    grade = State()
    sphere = State()
    description = State()
    wait = State()


DATA = """
Ваши данные
Имя:         {}
Уровень:     {}
Сфера:       {}
Описание: 
{}
"""


async def do_text(state: FSMContext):
    user_data = await state.get_data()
    n = user_data['name']
    g = user_data['grade']
    sp = user_data['sphere']
    d = user_data['description']
    call = user_data['call']
    if n != NoneData and g != NoneData and d != NoneData and sp != NoneData:
        await call.message.edit_text(text="Проверьте введенные данные и если все "
                                          "верно нажмите на соответсвующую кнопку \n\n" +
                                          DATA.format(n, g, sp, d),
                                     reply_markup=kb.reg_teacher_okay())
    else:
        await call.message.edit_text(DATA.format(n, g, sp, d),
                                     reply_markup=kb.reg_teacher(n, g, sp, d))


@dp.callback_query(lambda c: c.data == "teacher")
async def start_registration(call: CallbackQuery, state: FSMContext):
    user, i = check_id(call.from_user.id)
    if i == 0 or i == -1:
        await state.update_data(name=NoneData, grade=NoneData, sphere=NoneData, description=NoneData,
                                call=call)
    elif i == 1:
        await state.update_data(name=user.name, grade=user.grade, sphere=user.sphere,
                                description=user.description, call=call)
    await do_text(state)


@dp.callback_query(lambda c: c.data == "return_reg_teacher")
async def start_registration(call: CallbackQuery, state: FSMContext):
    await state.set_state(RegistrateTeacher.wait)
    await do_text(state)


@dp.callback_query(lambda c: c.data == "name_teacher")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Введите, как к вам обращаться", reply_markup=kb.reg_return_teacher())
    await state.set_state(RegistrateTeacher.name)


@dp.callback_query(lambda c: c.data == "grade_teacher")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Ввыберите ваш уровень", reply_markup=kb.grade_teacher())
    await state.set_state(RegistrateTeacher.grade)


@dp.callback_query(lambda c: c.data.split("_")[-2:] == ["grade", "teacher"])
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(grade=" ".join(callback_query.data.split("_")[:-2]).capitalize())
    await do_text(state)
    await state.set_state(RegistrateTeacher.wait)


@dp.callback_query(lambda c: c.data == "sphere_teacher")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    s = user_data['sphere']
    if s == NoneData:
        await callback_query.message.edit_text("Выберите ваши сферы деятельности", reply_markup=kb.sphere_teacher())
    else:
        await callback_query.message.edit_text("Выбрано " + s + "\nВыберите дополнительно или "
                                                                "нажмите повторно чтобы убрать",
                                               reply_markup=kb.sphere_teacher())
    await state.set_state(RegistrateTeacher.sphere)


@dp.callback_query(lambda c: c.data.split("_")[-2:] == ["sphere", "teacher"])
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    s = user_data['sphere']
    tt = " ".join(callback_query.data.split("_")[:-2])
    if s == NoneData:
        await state.update_data(sphere=tt)
    elif tt in s:
        tt = ", ".join([i for i in "".join(s.split(tt)).split(", ") if i != ""])
        await state.update_data(sphere=tt)
    else:
        tt = s + ", " + tt
        await state.update_data(sphere=tt)
    await callback_query.message.edit_text(text="Выбрано " + tt + "\nВыберите дополнительно или "
                                                                  "нажмите повторно чтобы убрать",
                                           reply_markup=kb.sphere_teacher())
    await state.set_state(RegistrateTeacher.wait)


@dp.callback_query(lambda c: c.data == "description_teacher")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Введите ваше описание", reply_markup=kb.reg_return_teacher())
    await state.set_state(RegistrateTeacher.description)


@dp.message(StateFilter(RegistrateTeacher.name))
async def text(message: Message, state: FSMContext):
    await state.update_data(name=message.text.capitalize())
    await message.delete()
    await do_text(state)
    await state.set_state(RegistrateTeacher.wait)


@dp.message(StateFilter(RegistrateTeacher.description))
async def text(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.delete()
    await do_text(state)
    await state.set_state(RegistrateTeacher.wait)


@dp.callback_query(lambda c: c.data == "reg_teacher_ok")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    n = user_data['name']
    g = user_data['grade']
    sp = user_data['sphere']
    d = user_data['description']
    call = user_data['call']
    await state.clear()
    user = teacher.model.Teacher(
        id=callback_query.from_user.id,
        name=n,
        grade=g,
        sphere=sp,
        description=d,
        show=False,
        nickname=callback_query.from_user.username
    )
    add_user(user)
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
