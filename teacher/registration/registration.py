"""Реализация регистрации"""
from aiogram.filters import StateFilter
# \registration
# 0) Учитель/ученик/both
# 1) Имя
# 2) Грейд: no_work, intern, junior, middle. senior
# 3) Сфера: NLP, CV,RecSys, Audio, Classic ML, любой
# 4) Текстовое описание себя
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

import teacher.registration.keyboard as kb
# from main import dp
from config import TOKEN_TG, dp, bot, router


class RegistrateTeacher(StatesGroup):
    name = State()
    surname = State()
    grade = State()
    sphere = State()
    description = State()
    wait = State()


DATA = """
Ваши данные
name        {}
surname      {}
grade {}
sphere {}
description {}
"""

FreeData = "null"


async def do_text(state: FSMContext):
    user_data = await state.get_data()
    n = user_data['name']
    s = user_data['surname']
    g = user_data['grade']
    sp = user_data['sphere']
    d = user_data['description']
    call = user_data['call']
    if (n != FreeData and s != FreeData and g != FreeData and d != FreeData and sp != FreeData):
        await call.message.edit_text(text="Проверьте введенные данные и если все "
                                          "верно нажмите на соответсвующую кнопку \n\n" +
                                          DATA.format(n, s, g, sp, d),
                                     reply_markup=kb.reg_teacher_okay())
    else:
        await call.message.edit_text(DATA.format(n, s, g, sp, d),
                                     reply_markup=kb.reg_teacher())


@dp.callback_query(lambda c: c.data == "teacher")
async def start_registration(call: CallbackQuery, state: FSMContext):
    await state.update_data(name=FreeData, surname=FreeData, grade=FreeData, sphere=FreeData, description=FreeData,
                            call=call)
    await do_text(state)


@dp.callback_query(lambda c: c.data == "return_reg_teacher")
async def start_registration(call: CallbackQuery, state: FSMContext):
    await state.set_state(RegistrateTeacher.wait)
    await do_text(state)


@dp.callback_query(lambda c: c.data == "name_teacher")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Введите ваше имя", reply_markup=kb.reg_return_teacher())
    await state.set_state(RegistrateTeacher.name)


@dp.callback_query(lambda c: c.data == "surname_teacher")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Введите ваше имя", reply_markup=kb.reg_return_teacher())
    await state.set_state(RegistrateTeacher.surname)


@dp.callback_query(lambda c: c.data == "grade_teacher")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Введите ваше имя", reply_markup=kb.grade_teacher())
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
    if s == FreeData:
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
    if s == FreeData:
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
    await callback_query.message.edit_text("Введите ваше имя", reply_markup=kb.reg_return_teacher())
    await state.set_state(RegistrateTeacher.description)


@dp.message(StateFilter(RegistrateTeacher.name))
async def text(message: Message, state: FSMContext):
    await state.update_data(name=message.text.capitalize())
    await message.delete()
    await do_text(state)
    await state.set_state(RegistrateTeacher.wait)


@dp.message(StateFilter(RegistrateTeacher.surname))
async def text(message: Message, state: FSMContext):
    await state.update_data(surname=message.text.capitalize())
    await message.delete()
    await do_text(state)
    await state.set_state(RegistrateTeacher.wait)


@dp.message(StateFilter(RegistrateTeacher.description))
async def text(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.delete()
    await do_text(state)
    await state.set_state(RegistrateTeacher.wait)

@dp.callback_query(lambda c: c.data == "cr_pr_ok")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    n = user_data['name']
    s = user_data['surname']
    call = user_data['call']
    await call.message.edit_text(text="Здраствуйте {} {}".format(n, s))
    await state.clear()

