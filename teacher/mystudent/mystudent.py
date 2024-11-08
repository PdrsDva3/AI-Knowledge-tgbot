from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import dp
from db.db_teacher import get_all_data_all_student


@dp.callback_query(lambda c: c.data == "my_students_teacher")
async def searching_next(callback: CallbackQuery):
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="start")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    students = await get_all_data_all_student(callback.from_user.id)
    TEACHER_LIST = "ваши студенты:"
    for student in students:
        TEACHER_LIST += (f"Имя:       {student["name"]}\n"
                         f"Уровень:   {student['grade']}\n"
                         f"Сфера:     {student['sphere']}\n"
                         f"Краткий рассказ: \n{student['description']}\n"
                         f"Для связи:  @{student['nickname']}\n\n")

    if TEACHER_LIST == "ваши студенты:":
        text = "У вас нет учеников"
    else:
        text = TEACHER_LIST
    await callback.message.edit_text(text, reply_markup=keyboard)
