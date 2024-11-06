import asyncio
import logging
import random

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.formatting import Bold, Text, as_list

from config import API_KEY, dp, bot
from db_requests import get_all, update_all, insert_all, get_all_teachers
import student.search.search
import student.search.keyboard
import student.registration.keyboard
import student.registration.registration
import student.search.filters


# @ dp.message(ContentType.PHOTO)
# async def handle_photo(message: Message, state: FSMContext):
#     print("Получена фотография")
#     photo_file_id = message.photo[-1].file_id
#     # Здесь можно добавить дополнительную логику для обработки фотографии
#
#     await message.answer(f"Спасибо за фотографию! Файл ID: {photo_file_id}")
#
#
# @ dp.message(ContentType.VIDEO)
# async def handle_video(message: Message, state: FSMContext):
#     print("Получено видео")
#     video_file_id = message.video.file_id
#     # Здесь можно добавить дополнительную логику для обработки видео
#
#     await message.answer(f"Спасибо за видео! Файл ID: {video_file_id}")
#
#
# @ dp.message(ContentType.DOCUMENT)
# async def handle_document(message: Message, state: FSMContext):
#     print("Получен документ")
#     document_file_id = message.document.file_id
#     # Здесь можно добавить дополнительную логику для обработки документа
#
#     await message.answer(f"Спасибо за документ! Файл ID: {document_file_id}")
#
#
# @ dp.message(ContentType.AUDIO)
# async def handle_audio(message: Message, state: FSMContext):
#     print("Получено аудио")
#     audio_file_id = message.audio.file_id
#     # Здесь можно добавить дополнительную логику для обработки аудио
#
#     await message.answer(f"Спасибо за аудио! Файл ID: {audio_file_id}")
#
#
# @ dp.message(ContentType.STICKER)
# async def handle_sticker(message: Message, state: FSMContext):
#     print("Получен стикер")
#     sticker_file_id = message.sticker.file_id
#     # Здесь можно добавить дополнительную логику для обработки стикера
#
#     await message.answer(f"Спасибо за стикер! Файл ID: {sticker_file_id}")
#
#
# @ dp.message(ContentType.VOICE)
# async def handle_voice(message: Message, state: FSMContext):
#     print("Получено голосовое сообщение")
#     voice_file_id = message.voice.file_id
#     # Здесь можно добавить дополнительную логику для обработки голосового сообщения
#
#     await message.answer(f"Спасибо за голосовое сообщение! Файл ID: {voice_file_id}")
#
#
# @ dp.message(ContentType.VIDEO_NOTE)
# async def handle_video_note(message: Message, state: FSMContext):
#     print("Получено видео-сообщение")
#     video_note_file_id = message.video_note.file_id
#     # Здесь можно добавить дополнительную логику для обработки видео-сообщения
#
#     await message.answer(f"Спасибо за видео-сообщение! Файл ID: {video_note_file_id}")


# todo text
# ========================================================================================================= keyboards
def starting_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="student", callback_data="info")],
        [InlineKeyboardButton(text="teacher", callback_data="teacher")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def info_and_continue_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Регистрация", callback_data="registration")],
        [InlineKeyboardButton(text="GO!", callback_data="cmd_go")],
        [InlineKeyboardButton(text="Список учителей", callback_data="teacher_list")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def return_go_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="cmd_go")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
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


# todo
# ======================================================================================================


@dp.message(Command("start"))
async def cmd_start(message: Message):
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


INFO_TEXT = """
Здесь ты можешь увидеть описание своих возможностей как студента.
        
    Регистрация/изменение данных - заполнить или изменить свою информацию.
    
    GO! - поиск учителей
    
    Список учителей - список всех принятых учителей
"""


@dp.callback_query(lambda query: query.data == "info")
async def student_info(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=INFO_TEXT,
        reply_markup=info_and_continue_kb()
    )


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
# todo
# реализовать список учителей
