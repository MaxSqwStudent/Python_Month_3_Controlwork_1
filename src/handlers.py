
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.keyboards import *
from src.State import *

router = Router()

users_data = {}

@router.message(CommandStart())
async def CommandStart(message: Message):
    await message.answer(
        f"Привет {message.from_user.full_name}!\n\n"
        f"Введи /help, чтобы получить список команд"
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "/start - команда для запуска\n"
        "/help - список команд\n"
        "/register - зарегистрировать пользователя\n"
        "/profile - показывает вашу информацию"
    )

@router.message(Command("register"))
async def cmd_about(message: Message, state: FSMContext):
    await message.answer(
        f"Регистрация пользователя:\n\n"
        f"Пожалуйста, введите ваше имя"
    )
    await state.set_state(User.waiting_name)


@router.message(Command("profile"))
async def cmd_about(message: Message, state: FSMContext):
    if message.from_user.id in users_data:
        print(users_data)
        user_data = users_data[message.from_user.id]
        await message.answer(
            f"Ваши данные:\n\n"
            f"Имя - {user_data['name']}\n"
            f"Возраст - {user_data['age']}"
        )
    else:
        await message.answer("Вы не зарегистрированы. Напишите /register, чтобы пройти регистрацию.")

@router.message(User.waiting_name)
async def quiz_message(message: Message, state: FSMContext):
    if message.text.isalpha():
        await message.answer(
            f"Ваше имя: {message.text}\n\n"
            f"Введите ваш возраст"
        )
        await state.update_data(name=message.text)
        await state.set_state(User.waiting_age)
    else:
        await message.answer(
            f"Пожалуйста, введите корректное имя (только буквы)"
        )

@router.message(User.waiting_age)
async def quiz_message(message: Message, state: FSMContext):
    if message.text.isdigit():
        if int(message.text) > 0:
            await state.update_data(age=message.text)
            data = await state.get_data()
            await message.answer(
                f"Регистрация завершена!\n\n"
                f"Ваше имя: {data['name']}\n"
                f"Ваш возраст: {message.text}\n\n"
                f"Сохранить данные?", reply_markup=inline_buttons
            )
        else:
            await message.answer(
                f"Пожалуйста, введите корректный возраст (только цифры)"
            ) 
    else:
        await message.answer(
            f"Пожалуйста, введите корректный возраст (только цифры)"
        ) 

@router.callback_query(F.data == "confirm_reg")
async def callback_confirm(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Регистрация завершена!")
    data = await state.get_data()
    name = data["name"]
    age = data["age"]
    user_id = callback.from_user.id
    users_data[user_id] = {"name": name, "age": age}
    await callback.message.answer("Регистрация завершена!")
    await state.clear()


@router.callback_query(F.data == "restart_reg")
async def callback_restart_reg(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Начало регистрации")
    await callback.message.answer(
            f"Регистрация пользователя:\n\n"
            f"Пожалуйста, введите ваше имя"
        )
    await state.set_state(User.waiting_name)