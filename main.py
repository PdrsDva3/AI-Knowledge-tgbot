from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.db import check_id
from teacher.registration import registration, keyboard
# from teacher.registration.registration import start_registration
from config import TOKEN_TG, dp, bot, router

@dp.message(StateFilter(None), Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user, i = check_id(message.from_user.id)
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
                InlineKeyboardButton(text="continue", callback_data="reg_teacher_ok"),
            ]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        DATA = """
        Здраствуйте,
        name        {}
        surname      {}
        grade {}
        sphere {}
        description {}
        """
        await message.answer(DATA.format(user.name, user.surname, user.grade, user.sphere, user.description), reply_markup=keyboard)


if __name__ == "__main__":
    dp.run_polling(bot)
