from pydantic import BaseModel, EmailStr, field_validator
import re

class Feedback(BaseModel):
    name: str
    email: str
    phone: str
    message: str
    rating: int | None = None

    @field_validator('email')
    def validate_email(cls, v):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Некорректный email')
        return v

    @field_validator('phone')
    def validate_phone(cls, v):
        if not re.match(r'^8\d{10}$', v):
            raise ValueError('Телефон должен начинаться с 8 и содержать 11 цифр')
        return v

# Хранение отзывов в памяти (в реальном проекте используйте БД)
feedbacks = []