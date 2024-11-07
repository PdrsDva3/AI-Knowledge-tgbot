import asyncio
import logging

from aiogram.types import Message

from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

import db.migration
from db.db_teacher import check_id
from config import dp, bot

import db.migration

import student.registration.registration
import student.search.search
import student.search.filters

import teacher.registration.registration
import teacher.search.search
import teacher.setting.setting
import teacher.search.filters
import teacher.mystudent.mystudent


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
        [InlineKeyboardButton(text="Список учителей", callback_data="teacher_list")],
        [InlineKeyboardButton(text="return", callback_data="return_to_start")]
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


# ======================================================================================================

@dp.callback_query(lambda c: c.data == "start")
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    user, i = check_id(callback_query.from_user.id)
    if i == 0:
        kb = [
            [
                InlineKeyboardButton(text="Регистрация", callback_data="teacher"),
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
            ],
            [InlineKeyboardButton(text="return", callback_data="return_to_start")]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        DATA = """
                Здраствуйте,
                Имя        {}
                Уровень       {}
                Сфера      {}
                Описание {}
                """
        await callback_query.message.edit_text(
            DATA.format(user.name, user.grade, user.sphere, user.description),
            reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "return_to_start")
async def cmd_start(callback_query: CallbackQuery):
    kb = [
        [InlineKeyboardButton(text="student", callback_data="info")],
        [InlineKeyboardButton(text="teacher", callback_data="start")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await callback_query.message.edit_text("Здраствуйте", reply_markup=keyboard)


INFO_TEXT = """
Здесь ты можешь увидеть описание своих возможностей как студента.
        
    Регистрация/изменение данных - заполнить или изменить свою информацию.
    
    GO! - поиск учителей
    
    Список учителей - список всех принятых учителей
"""


@dp.message(Command("start"))
async def cmd_start(message: Message):
    kb = [
        [InlineKeyboardButton(text="student", callback_data="info")],
        [InlineKeyboardButton(text="teacher", callback_data="start")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("Здраствуйте", reply_markup=keyboard)


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
    # db.migration.migration_down()
    db.migration.migration_up()
    asyncio.run(main())

# 1)
# todo сделать поиск с учетом фильтров

# 2)
# todo реализовать отправление-принятие заявки
# todo реализовать список учителей

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
