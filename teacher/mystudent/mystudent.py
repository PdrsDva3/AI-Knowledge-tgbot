from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import dp
from db.db_teacher import get_all_student


@dp.callback_query(lambda c: c.data == "my_students_teacher")
async def searching_next(callback: CallbackQuery):
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="start")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    students = await get_all_student(callback.from_user.id)
    text = "ваши студенты:\n"+"\n".join([student["name"] for student in students])
    await callback.message.edit_text(text, reply_markup=keyboard)