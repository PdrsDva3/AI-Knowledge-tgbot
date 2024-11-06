from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

import db.migration
from db.db import check_id
from teacher.registration import registration, keyboard
from teacher.setting import setting, keyboard
# from teacher.registration.registration import start_registration
from config import TOKEN_TG, dp, bot, router


# 1) \settings_teacher - установка настроек
# 2) \get_students - получить список учеников в очереди, сортированных по \settings
# 3) \start - описание ручек
# 4) \registration - изменить свою анкету
# 5) \all_students - список всех принятых студентов

@dp.message(StateFilter(None), Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user, i = check_id(message.from_user.id)
    print(i, message.from_user.id)
    if i == 0:
        kb = [
            [
                InlineKeyboardButton(text="teacher", callback_data="teacher"),
            ]]

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        await message.answer("Здраствуйте, пройдите регистрацию", reply_markup=keyboard)
    else:
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
            ]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        DATA = """
                Здраствуйте,
                name        {}
                surname     {}
                grade       {}
                sphere      {}
                description {}
                """
        await message.answer(DATA.format(user.name, user.surname, user.grade, user.sphere, user.description),
                             reply_markup=keyboard)



@dp.callback_query(lambda c: c.data == "start")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    user, i = check_id(callback_query.from_user.id)
    if i == 0:
        kb = [
            [
                InlineKeyboardButton(text="teacher", callback_data="teacher"),
            ]]

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        await callback_query.message.edit_text("Здраствуйте, пройдите регистрацию", reply_markup=keyboard)
    else:
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
            ]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        DATA = """
                Здраствуйте,
                name        {}
                surname     {}
                grade       {}
                sphere      {}
                description {}
                """
        await callback_query.message.edit_text(DATA.format(user.name, user.surname, user.grade, user.sphere, user.description),
                             reply_markup=keyboard)

if __name__ == "__main__":
    db.migration.migration_down()
    db.migration.migration_up()
    dp.run_polling(bot)
