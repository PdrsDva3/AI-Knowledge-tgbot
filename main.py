from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from teacher.registration import registration, keyboard
# from teacher.registration.registration import start_registration
from config import TOKEN_TG, dp, bot, router

@dp.message(StateFilter(None), Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    kb = [
        [
            InlineKeyboardButton(text="teacher", callback_data="teacher"),
        ]]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("Здраствуйте", reply_markup=keyboard)


if __name__ == "__main__":
    dp.run_polling(bot)
