from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.markdown import hbold
import re
from datetime import datetime

import app.keyboards as kb
from app.database import Database

router = Router()
db = Database()


class FeedbackStates(StatesGroup):
    rating = State()
    name = State()
    email = State()
    phone = State()
    message = State()


async def show_main_menu(message: Message):
    await message.answer("Выберите действие:", reply_markup=kb.main)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Приветствую, это телеграм бот от компании 30бит!\n"
        "Здесь вы можете оставить обратную связь нашей компании",
        reply_markup=kb.main
    )


@router.message(F.text == 'Вернуться в меню')
async def back_to_menu(message: Message):
    await show_main_menu(message)


@router.message(F.text == 'О компании')
async def about_company(message: Message):
    await message.answer(
        "Компания 30бит - лидер в IT-решениях с 2010 года.\n"
        "Мы предоставляем инновационные продукты и качественный сервис.",
        reply_markup=kb.back_to_menu
    )


@router.message(F.text == 'Обратная связь')
async def start_feedback(message: Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, оцените нашу компанию:",
        reply_markup=kb.mark
    )
    await state.set_state(FeedbackStates.rating)


@router.callback_query(F.data.in_(['one', 'two', 'three', 'four', 'five']), FeedbackStates.rating)
async def process_rating(callback: CallbackQuery, state: FSMContext):
    rating_map = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5
    }

    rating = rating_map[callback.data]
    stars = '⭐' * rating

    try:
        await callback.message.delete()
    except:
        pass

    await state.update_data(rating=rating)
    await callback.answer(f"Вы поставили оценку {rating} {stars}")

    await callback.message.answer(
        f"Спасибо за оценку {stars}!\n"
        "Теперь введите ваше имя:",
        reply_markup=kb.back_to_menu
    )
    await state.set_state(FeedbackStates.name)


@router.message(F.text == 'Список отзывов')
async def show_feedbacks(message: Message):
    feedbacks = db.get_feedbacks()
    if not feedbacks:
        await message.answer("Пока нет отзывов.", reply_markup=kb.back_to_menu)
        return

    response = "📝 Список отзывов:\n\n"
    for i, feedback in enumerate(feedbacks, 1):
        stars = '⭐' * feedback['rating']
        response += (
            f"{hbold(f'Отзыв #{i}')}\n"
            f"Оценка: {stars}\n"
            f"Имя: {feedback['name']}\n"
            f"Сообщение: {feedback['message']}\n"
            f"Дата: {datetime.strptime(feedback['created_at'], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')}\n\n"
        )

    await message.answer(response, reply_markup=kb.back_to_menu)


@router.message(FeedbackStates.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Теперь введите ваш email (пример: example@mail.com):")
    await state.set_state(FeedbackStates.email)


@router.message(FeedbackStates.email)
async def process_email(message: Message, state: FSMContext):
    email = message.text
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        await message.answer("Некорректный email. Пожалуйста, введите email в формате example@mail.com:")
        return

    await state.update_data(email=email)
    await message.answer("Теперь введите ваш телефон (начинается с 8, 11 цифр, например: 89123456789):")
    await state.set_state(FeedbackStates.phone)


@router.message(FeedbackStates.phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text
    if not re.match(r'^8\d{10}$', phone):
        await message.answer("Некорректный телефон. Введите номер начинающийся с 8 и содержащий 11 цифр:")
        return

    await state.update_data(phone=phone)
    await message.answer("Напишите ваше сообщение:")
    await state.set_state(FeedbackStates.message)


@router.message(FeedbackStates.message)
async def process_message(message: Message, state: FSMContext):
    data = await state.get_data()
    data['message'] = message.text

    # Сохраняем в базу данных
    db.add_feedback(data)

    stars = '⭐' * data['rating']
    response = (
        "✅ Спасибо за обратную связь!\n\n"
        f"{hbold('Ваши данные:')}\n"
        f"Оценка: {stars}\n"
        f"Имя: {data['name']}\n"
        f"Email: {data['email']}\n"
        f"Телефон: {data['phone']}\n"
        f"Сообщение: {data['message']}\n\n"
        "Мы обязательно рассмотрим ваше обращение!"
    )

    await message.answer(response, reply_markup=kb.back_to_menu)
    await state.clear()