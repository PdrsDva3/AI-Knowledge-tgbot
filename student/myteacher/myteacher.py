"""
Вывод списка учителей для 'студента'
"""
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import dp, bot
from db.db_student import get_teacher_list


@dp.callback_query(lambda query: query.data == "teacher_list")
async def student_info(callback: CallbackQuery):
    list_ = await get_teacher_list(callback.from_user.id)

    TEACHER_LIST = "Список ваших учителей:\n"
    if list_:
        for tch in list_:
            TEACHER_LIST += (f"Имя: \t\t\t\t{tch["name"]}\n"
                             f"Уровень: \t\t\t\t{tch['grade']}\n"
                             f"Сфера: \t\t\t\t{tch['sphere']}\n"
                             f"Краткий рассказ: \n{tch['description']}\n"
                             f"Для связи: \t\t\t\t{tch['nickname']}\n\n")
    else:
        TEACHER_LIST = "У вас пока нет учителей"

    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="info")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=TEACHER_LIST,
        reply_markup=keyboard
    )