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
    STUDENT_LIST = "ваши студенты:\n"
    for student in students:
        STUDENT_LIST += (f"Имя:       {student["name"]}\n"
                         f"Уровень:   {student['grade']}\n"
                         f"Сфера:     {student['sphere']}\n"
                         f"Краткий рассказ: \n{student["bio"]}\n"
                         f"Для связи:  @{student['nickname']}\n\n")

    if STUDENT_LIST == "ваши студенты:":
        text = "У вас нет учеников"
    else:
        text = STUDENT_LIST
    await callback.message.edit_text(text, reply_markup=keyboard)
