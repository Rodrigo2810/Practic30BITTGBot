from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

# Главное меню
main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='О компании')],
        [KeyboardButton(text='Обратная связь')],
        [KeyboardButton(text='Список отзывов')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню:'
)

# Кнопка возврата в главное меню
back_to_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Вернуться в меню')]],
    resize_keyboard=True
)

# Оценки
mark = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='⭐ (1)', callback_data='one')],
        [InlineKeyboardButton(text='⭐⭐ (2)', callback_data='two')],
        [InlineKeyboardButton(text='⭐⭐⭐ (3)', callback_data='three')],
        [InlineKeyboardButton(text='⭐⭐⭐⭐ (4)', callback_data='four')],
        [InlineKeyboardButton(text='⭐⭐⭐⭐⭐ (5)', callback_data='five')]
    ]
)