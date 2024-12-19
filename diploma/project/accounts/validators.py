from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re


# Валидатор для уникальности email
def validate_unique_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError("Пользователь с такой почтой уже зарегистрирован.")

# Валидатор, чтобы в поле email не вводились русские буквы
def validate_no_russian_in_email(value):
    if re.search(r'[а-яА-Я]', value):
        raise ValidationError("Email не должен содержать русские буквы.")

# Валидатор для уникальности password
def validate_password_not_in_use(value):
    users = User.objects.all()
    for user in users:
        if user.password and check_password(value, user.password):
            raise ValidationError("Этот пароль уже используется другим пользователем. Выберите другой.")


# Валидатор для длины пароля
def validate_password_length(value):
    if len(value) < 8:
        raise ValidationError("Пароль должен содержать минимум 8 символов.")


# Валидатор для проверки спецсимволов в first_name и last_name
def validate_no_special_characters(value):
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError("Имя и фамилия не должны содержать специальных символов.")


# Валидатор для допустимых форматов файлов
def validate_file_format(file):
    allowed_formats = ['csv', 'json']
    if not file.name.split('.')[-1] in allowed_formats:
        raise ValidationError(f"Недопустимый формат файла. Разрешены только: {', '.join(allowed_formats)}.")


