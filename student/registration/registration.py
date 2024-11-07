"""
Реализация регистрации 'студента'
"""
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from config import dp, bot
from db.db_student import get_all, update_all, insert_all
from student.registration import keyboard as kb


class Registration(StatesGroup):
    name = State()
    grade = State()
    sphere = State()
    bio = State()
    wait = State()


DATA = """
Для продолжения было бы славно заполнить анкету))

Ваша информация на данный момент:

Имя:    {}
Уровень:    {}
Сфера:  {}
Краткий рассказ:
{}
"""

NoneData = ""


async def print_text(state: FSMContext):
    user_data = await state.get_data()

    n = user_data['name']
    g = user_data['grade']
    s = user_data['sphere']
    b = user_data['bio']

    call = user_data['call']
    if n != NoneData and g != NoneData and s != NoneData and b != NoneData:
        await call.message.edit_text(text="Проверьте введенные данные и если все "
                                          "верно нажмите на соответсвующую кнопку \n\n" +
                                          DATA.format(n, g, s, b),
                                     reply_markup=kb.registration_okay_kb())
    else:
        await call.message.edit_text(DATA.format(n, g, s, b),
                                     reply_markup=kb.dynamic_choosing_kb(n, g, s, b))  # kb.registration_kb() - была,
                                                                                # но она без галочек, Денчику не кайф


# пример user_info [{'id': 574957210, 'role': 'student', 'name': 'Денис', 'grade': 'No work', 'sphere': 'Any', 'bio': 'Я хотдог'}]
@dp.callback_query(lambda c: c.data == "registration")
async def cmd_registration(callback: CallbackQuery, state: FSMContext):
    user_info = await get_all(callback.from_user.id)
    if user_info:
        user_info = user_info[0]
        await state.update_data(name=user_info["name"], grade=user_info["grade"], sphere=user_info["sphere"],
                                bio=user_info["bio"], call=callback)
    else:
        await state.update_data(name=NoneData, grade=NoneData, sphere=NoneData, bio=NoneData, call=callback)

    await print_text(state)


@dp.callback_query(lambda c: c.data == "return")
async def start_registration(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.wait)
    await print_text(state)


@dp.callback_query(lambda c: c.data == "name")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Введите ваше имя", reply_markup=kb.return_kb())
    await state.set_state(Registration.name)
    await state.update_data(call=callback_query)


# !!!!!!!! grade choice
@dp.callback_query(lambda c: c.data == "grade")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Выберите уровень подготовки", reply_markup=kb.choose_grade_kb())
    await state.set_state(Registration.grade)


@dp.callback_query(lambda c: c.data.split("_")[-1] == "grade")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(grade=" ".join(callback_query.data.split("_")[:-1]).capitalize())
    await print_text(state)
    await state.set_state(Registration.wait)


# !!!!!!!!


# ///////////// sphere choice
@dp.callback_query(lambda c: c.data == "sphere")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    s = user_data['sphere']
    if s == NoneData:
        await callback_query.message.edit_text("Выберите ваши сферы деятельности", reply_markup=kb.choose_sphere_kb())
    else:
        await callback_query.message.edit_text("Выбрано " + s + "\nВыберите дополнительно или "
                                                                "нажмите повторно чтобы убрать",
                                               reply_markup=kb.choose_sphere_kb())
    await state.set_state(Registration.sphere)


@dp.callback_query(lambda c: c.data.split("_")[-1] == "sphere")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    s = user_data['sphere']
    tt = " ".join(callback_query.data.split("_")[:-1])
    if s == NoneData:
        await state.update_data(sphere=tt)
    elif tt in s:
        tt = ", ".join([i for i in "".join(s.split(tt)).split(", ") if i != ""])
        await state.update_data(sphere=tt)
    else:
        tt = s + ", " + tt
        await state.update_data(sphere=tt)
    await callback_query.message.edit_text(text="Выбрано " + tt + "\nВыберите дополнительно или\n "
                                                                  "нажмите повторно чтобы убрать",
                                           reply_markup=kb.choose_sphere_kb())
    await state.set_state(Registration.wait)


# /////////////

@dp.callback_query(lambda c: c.data == "bio")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Введите краткий рассказ", reply_markup=kb.return_kb())
    await state.set_state(Registration.bio)
    await state.update_data(call=callback_query)


@dp.message(StateFilter(Registration.name))
async def text(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.delete()
    await print_text(state)
    await state.set_state(Registration.wait)


@dp.message(StateFilter(Registration.bio))
async def text(message: Message, state: FSMContext):
    await state.update_data(bio=message.text)
    await message.delete()
    await print_text(state)
    await state.set_state(Registration.wait)


ALL_OKAY_TEXT = """
Регистрация успешно завершена.
Все изменения внесены)
    
    Регистрация/изменение данных - заполнить или изменить свою информацию.
    
    GO! - поиск учителей
    
    Список учителей - список всех принятых учителей
"""


@dp.callback_query(lambda c: c.data == "all_is_okay")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    user_data = await state.get_data()
    if await get_all(user_id):
        await update_all(user_id, user_data["name"], user_data["grade"], user_data["sphere"],
                         user_data["bio"])
    else:
        await insert_all(user_id,  user_data["name"], user_data["grade"], user_data["sphere"],
                         user_data["bio"], callback_query.from_user.username)

    await state.clear()
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=ALL_OKAY_TEXT,
        reply_markup=kb.info_and_continue_kb()
    )
