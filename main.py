import asyncio
import logging
import random

from aiogram import Bot, Dispatcher, types
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.formatting import Bold, Text, as_list

from config import API_KEY
from db_requests import get_all, update_all, insert_all, get_all_teachers

API_KEY = API_KEY

bot = Bot(token=API_KEY)
dp = Dispatcher()


# todo
# ========================================================================================================= keyboards
def starting_kb() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="student", callback_data="info")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def info_and_continue_kb() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Регистрация", callback_data="registration")],
        [types.InlineKeyboardButton(text="GO!", callback_data="cmd_go")],
        [types.InlineKeyboardButton(text="Список учителей", callback_data="teacher_list")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def registration_kb() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Имя", callback_data="name")],
        [types.InlineKeyboardButton(text="Уровень", callback_data="grade")],
        [types.InlineKeyboardButton(text="Сфера", callback_data="sphere")],
        [types.InlineKeyboardButton(text="Краткий рассказ", callback_data="bio")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def registration_okay_kb() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Имя", callback_data="name")],
        [types.InlineKeyboardButton(text="Уровень", callback_data="grade")],
        [types.InlineKeyboardButton(text="Сфера", callback_data="sphere")],
        [types.InlineKeyboardButton(text="Краткий рассказ", callback_data="bio")],
        [types.InlineKeyboardButton(text="Назад (без сохранения)", callback_data="info"),
        types.InlineKeyboardButton(text="Сохранить", callback_data="all_is_okay")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# NLP, CV,RecSys, Audio, Classic ML, любой
def choose_sphere_kb() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="NLP", callback_data="NLP_sphere")],
        [types.InlineKeyboardButton(text="CV", callback_data="CV_sphere")],
        [types.InlineKeyboardButton(text="RecSys", callback_data="RecSys_sphere")],
        [types.InlineKeyboardButton(text="Audio", callback_data="Audio_sphere")],
        [types.InlineKeyboardButton(text="Classic ML", callback_data="Classic_ML_sphere")],
        [types.InlineKeyboardButton(text="Любой", callback_data="Any_sphere")],
        [types.InlineKeyboardButton(text="Назад", callback_data="return")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# no_work, intern, junior, middle. senior
def choose_grade_kb() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="No work", callback_data="no_work_grade")],
        [types.InlineKeyboardButton(text="Intern", callback_data="intern_grade")],
        [types.InlineKeyboardButton(text="Junior", callback_data="junior_grade")],
        [types.InlineKeyboardButton(text="Middle", callback_data="middle_grade")],
        [types.InlineKeyboardButton(text="Senior", callback_data="senior_grade")],
        [types.InlineKeyboardButton(text="Назад", callback_data="return")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def return_kb() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Назад", callback_data="return")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def return_go_kb() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Назад", callback_data="cmd_go")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def search_or_filters_kb() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Искать без фильтров", callback_data="search")],
        [types.InlineKeyboardButton(text="Искать с фильтрами", callback_data="filters")],
        [types.InlineKeyboardButton(text="Назад", callback_data="info")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def searching_kb() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Принять", callback_data="agree"),
         types.InlineKeyboardButton(text="Вперед", callback_data="next_teacher")
         ],
        [types.InlineKeyboardButton(text="Назад", callback_data="cmd_go")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
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


def fsearching_kb() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="Принять", callback_data="agree"),
         types.InlineKeyboardButton(text="Вперед", callback_data="fnext_teacher")],
        [types.InlineKeyboardButton(text="Назад", callback_data="filters")]

    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def fchoose_sphere_kb() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="NLP", callback_data="NLP_spheref")],
        [types.InlineKeyboardButton(text="CV", callback_data="CV_spheref")],
        [types.InlineKeyboardButton(text="RecSys", callback_data="RecSys_spheref")],
        [types.InlineKeyboardButton(text="Audio", callback_data="Audio_spheref")],
        [types.InlineKeyboardButton(text="Classic ML", callback_data="Classic_ML_spheref")],
        [types.InlineKeyboardButton(text="Любой", callback_data="Any_spheref")],
        [types.InlineKeyboardButton(text="Назад", callback_data="returnf")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# no_work, intern, junior, middle. senior
def fchoose_grade_kb() -> InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(text="No work", callback_data="no_work_gradef")],
        [types.InlineKeyboardButton(text="Intern", callback_data="intern_gradef")],
        [types.InlineKeyboardButton(text="Junior", callback_data="junior_gradef")],
        [types.InlineKeyboardButton(text="Middle", callback_data="middle_gradef")],
        [types.InlineKeyboardButton(text="Senior", callback_data="senior_gradef")],
        [types.InlineKeyboardButton(text="Назад", callback_data="returnf")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# todo
# ======================================================================================================


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
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

INFO_TEXT="""
Здесь ты можешь увидеть описание своих возможностей как студента.
        
    Регистрация/изменение данных - заполнить или изменить свою информацию.
    
    GO! - поиск учителей
    
    Список учителей - список всех принятых учителей
"""

@dp.callback_query(lambda query: query.data == "info")
async def student_info(callback: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=INFO_TEXT,
        reply_markup=info_and_continue_kb()
    )


# ----------------------------------------------------------------------------------------------------------------- registration
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
                                     reply_markup=registration_okay_kb())
    else:
        await call.message.edit_text(DATA.format(n, g, s, b),
                                     reply_markup=registration_kb())


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
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Введите ваше имя", reply_markup=return_kb())
    await state.set_state(Registration.name)
    await state.update_data(call=callback_query)


# !!!!!!!! grade choice
@dp.callback_query(lambda c: c.data == "grade")
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Выберите уровень подготовки", reply_markup=choose_grade_kb())
    await state.set_state(Registration.grade)


@dp.callback_query(lambda c: c.data.split("_")[-1] == "grade")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(grade=" ".join(callback_query.data.split("_")[:-1]).capitalize())
    await print_text(state)
    await state.set_state(Registration.wait)


# !!!!!!!!


# ///////////// sphere choice
@dp.callback_query(lambda c: c.data == "sphere")
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    s = user_data['sphere']
    if s == NoneData:
        await callback_query.message.edit_text("Выберите ваши сферы деятельности", reply_markup=choose_sphere_kb())
    else:
        await callback_query.message.edit_text("Выбрано " + s + "\n\nВыберите дополнительно или "
                                                                "нажмите повторно чтобы убрать",
                                               reply_markup=choose_sphere_kb())
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
                                           reply_markup=choose_sphere_kb())
    await state.set_state(Registration.wait)


# /////////////

@dp.callback_query(lambda c: c.data == "bio")
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Введите краткий рассказ", reply_markup=return_kb())
    await state.set_state(Registration.bio)
    await state.update_data(call=callback_query)


@dp.message(StateFilter(Registration.name))
async def text(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.delete()
    await print_text(state)
    await state.set_state(Registration.wait)


@dp.message(StateFilter(Registration.bio))
async def text(message: types.Message, state: FSMContext):
    await state.update_data(bio=message.text)
    await message.delete()
    await print_text(state)
    await state.set_state(Registration.wait)

ALL_OKAY_TEXT="""
Регистрация успешно завершена. Все изменения внесены)
            
    Регистрация/изменение данных - заполнить или изменить свою информацию.
    
    GO! - поиск учителей
    
    Список учителей - список всех принятых учителей
"""

@dp.callback_query(lambda c: c.data == "all_is_okay")
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    user_data = await state.get_data()
    if await get_all(user_id):
        await update_all(user_id, "student", user_data["name"], user_data["grade"], user_data["sphere"],
                         user_data["bio"])
    else:
        await insert_all(user_id, "student", user_data["name"], user_data["grade"], user_data["sphere"],
                         user_data["bio"], callback_query.from_user.username)

    await state.clear()
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=ALL_OKAY_TEXT,
        reply_markup=info_and_continue_kb()
    )


# =========================================------------------------------------------------------------------ GO! (without filter)
@dp.callback_query(lambda c: c.data == "cmd_go")
async def cmd_go(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="""
            Ты можешь выставить определенные фильтры \nили искать по всем подряд
            """,
        reply_markup=search_or_filters_kb()
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


async def print_teacher(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    teacher_list = data.get("list", [])
    index = data.get("index", 0)

    if index < len(teacher_list):
        teacher = teacher_list[index]
        await callback.message.edit_text(
            text=TEACHER_DATA.format(teacher["name"], teacher["grade"], teacher["sphere"], teacher["bio"]),
            reply_markup=searching_kb()
        )
    else:
        await state.clear()
        await callback.message.edit_text(
            text="Учителя закончились((",
            reply_markup=return_go_kb()
        )


@dp.callback_query(lambda c: c.data == "search")
async def searching(callback: types.CallbackQuery, state: FSMContext):
    teacher_data = await state.get_data()
    if "list" not in teacher_data:
        random_list = await get_random_teachers()
        await state.update_data(list=random_list, index=0)
        await print_teacher(callback, state)


@dp.callback_query(lambda c: c.data == "next_teacher")
async def searching_next(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data.get("index", 0) + 1

    await state.update_data(index=index)
    await print_teacher(callback, state)


# =========================================------------------------------------------------------------------ GO! (with filter)

class Filters(StatesGroup):
    grade = State()
    sphere = State()
    wait = State()


FILTER_DATA = """
В данный момент выбраны фильтры:

Уровень:   {}

Сфера:   {}
"""


async def print_filters(state: FSMContext):
    filter_data = await state.get_data()

    g = filter_data['grade']
    s = filter_data['sphere']

    call = filter_data['call']
    await call.message.edit_text(text=FILTER_DATA.format(g, s),
                                 reply_markup=cmd_filters_kb())


@dp.callback_query(lambda c: c.data == "filters")
async def cmd_filters(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(grade=NoneData, sphere=NoneData, call=callback)
    await print_filters(state)


@dp.callback_query(lambda c: c.data == "returnf")
async def choice_returning(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Filters.wait)
    await print_filters(state)


# !!!!!!!! grade choice
@dp.callback_query(lambda c: c.data == "gradef")
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Выберите уровень подготовки", reply_markup=fchoose_grade_kb())
    await state.set_state(Filters.grade)


@dp.callback_query(lambda c: c.data.split("_")[-1] == "gradef")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(grade=" ".join(callback_query.data.split("_")[:-1]).capitalize())
    await print_filters(state)
    await state.set_state(Filters.wait)


# !!!!!!!!


# ///////////// sphere choice
@dp.callback_query(lambda c: c.data == "spheref")
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    filter_data = await state.get_data()
    s = filter_data['sphere']
    if s == NoneData:
        await callback_query.message.edit_text("Выберите ваши сферы деятельности", reply_markup=fchoose_sphere_kb())
    else:
        await callback_query.message.edit_text("Выбрано " + s + "\n\nВыберите дополнительно или "
                                                                "нажмите повторно чтобы убрать",
                                               reply_markup=fchoose_sphere_kb())
    await state.set_state(Filters.sphere)


@dp.callback_query(lambda c: c.data.split("_")[-1] == "spheref")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    filter_data = await state.get_data()
    s = filter_data['sphere']
    tt = " ".join(callback_query.data.split("_")[:-1])
    if s == NoneData:
        await state.update_data(sphere=tt)
    elif tt in s:
        tt = ", ".join([i for i in "".join(s.split(tt)).split(", ") if i != ""])
        await state.update_data(sphere=tt)
    else:
        tt = s + ", " + tt
        await state.update_data(sphere=tt)
    await callback_query.message.edit_text(text="Выбрано " + tt + "\n\nВыберите дополнительно или\n "
                                                                  "нажмите повторно чтобы убрать",
                                           reply_markup=fchoose_sphere_kb())
    await state.set_state(Filters.wait)


# /////////////

async def get_random_teachersf() -> list[dict]:
    list_ = await get_all_teachers()
    random.shuffle(list_)
    return list_


TEACHER_DATAf = """
Имя:    {}
Уровень:    {}
Сфера:    {}
Краткий рассказ:
{}
"""


async def print_teacherf(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    teacher_list = data.get("list", [])
    index = data.get("index", 0)

    if index < len(teacher_list):
        teacher = teacher_list[index]
        await callback.message.edit_text(
            text=TEACHER_DATAf.format(teacher["name"], teacher["grade"], teacher["sphere"], teacher["bio"]),
            reply_markup=fsearching_kb()
        )
    else:
        await state.clear()
        await callback.message.edit_text(
            text="Учителя закончились((",
            reply_markup=return_go_kb()
        )


@dp.callback_query(lambda c: c.data == "fsearch")
async def searching(callback: types.CallbackQuery, state: FSMContext):
    teacher_data = await state.get_data()  # todo прочитать из стейта grade и sphere и НАПИСАТЬ SQL-ЗАПРОС с импользованием фильтров
    if "list" not in teacher_data:
        random_list = await get_random_teachersf()
        await state.update_data(list=random_list, index=0)
        await print_teacherf(callback, state)


@dp.callback_query(lambda c: c.data == "fnext_teacher")
async def searching_next(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data.get("index", 0) + 1

    await state.update_data(index=index)
    await print_teacherf(callback, state)


# -=-=-=-=-=-=-=---=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-==-=-= running
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
# todo реализовать список учителей
