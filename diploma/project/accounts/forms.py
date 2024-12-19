from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .validators import (
    validate_password_not_in_use,
    validate_unique_email,
    validate_password_length,
    validate_no_special_characters,
    validate_no_russian_in_email,
    validate_file_format
)
from .models import UploadedFile
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Имя",
        validators=[validate_no_special_characters])

    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Фамилия",
        validators=[validate_no_special_characters],
    )
    email = forms.CharField(
        max_length=254,
        required=True,
        label="Почта",
        validators=[validate_unique_email, validate_no_russian_in_email],
    )
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        validators=[validate_password_length, validate_password_not_in_use],
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        validators=[validate_password_length],
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_password2(self):
        """Проверяем, что password1 и password2 совпадают."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
    )

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

    file = forms.FileField(
        validators=[validate_file_format],
        label="Загрузите файл",
    )


