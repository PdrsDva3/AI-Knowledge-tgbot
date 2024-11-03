import asyncio
import logging
from pkgutil import get_data

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.formatting import Bold, Text, as_marked_list, as_list
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import F
# from netaddr.ip.iana import query

from config import API_KEY
from db_requests import get_all, update_all, insert_all

API_KEY = API_KEY

bot = Bot(token=API_KEY)
dp = Dispatcher()


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
        [types.InlineKeyboardButton(text="GO!", callback_data="go")],
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
        [types.InlineKeyboardButton(text="Всё верно", callback_data="all_is_okay")],
        [types.InlineKeyboardButton(text="Назад (нажимая после изменений, они не сохранятся)", callback_data="info")],
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


@dp.callback_query(lambda query: query.data == "info")
async def student_info(callback: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="""
        Здесь ты можешь увидеть описание своих возможностей как студента.
        
        Регистрация/изменение данных - заполнить или изменить свою информацию.
        
        GO! - поиск учителей
        
        Список учителей - список всех принятых учителей
        """,
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

# [{'id': 574957210, 'role': 'student', 'name': 'Денис', 'grade': 'No work', 'sphere': 'Any', 'bio': 'Я хотдог'}]
@dp.callback_query(lambda c: c.data == "registration")
async def cmd_registration(callback: CallbackQuery, state: FSMContext):
    user_info = (await get_all(callback.from_user.id))[0]
    if user_info:
        await state.update_data(name=user_info["name"], grade=user_info["grade"], sphere=user_info["sphere"], bio=user_info["bio"], call=callback)
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
        await callback_query.message.edit_text("Выбрано " + s + "\nВыберите дополнительно или "
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


##################################################################################################### state processing
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


# ----------------------------------------------------------
@dp.callback_query(lambda c: c.data == "all_is_okay")
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    user_data = await state.get_data()
    if await get_all(user_id):
        await update_all(user_id, "student", user_data["name"], user_data["grade"], user_data["sphere"], user_data["bio"])
    else:
        await insert_all(user_id, "student", user_data["name"], user_data["grade"], user_data["sphere"], user_data["bio"])


    await state.clear()
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="""
            Регистрация успешно завершена.
            Все изменения внесены)
            """,
        reply_markup=info_and_continue_kb()
    )


# -=-=-=-=-=-=-=---=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-==-=-= running
logging.basicConfig(level=logging.DEBUG)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
