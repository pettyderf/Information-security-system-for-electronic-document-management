from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логин')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    email = forms.CharField(label='Почта')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Пароли не совпадают")
        return cd['password2']


# ШИФРОВАНИЕ
class DH_key_exchange(forms.Form):
    user_tag = forms.CharField(label='Логин пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class DH_accept_key_exchange(forms.Form):
    user_tag = forms.CharField(label='Логин пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class CriptGostForm(forms.Form):
    opentext = forms.CharField(label='Открытый текст', widget=forms.Textarea)
    user_tag = forms.CharField(label='Логин пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class DecriptMagmaForm(forms.Form):
    file = forms.FileField(label='Зашифрованное сообщение')
    user_tag = forms.CharField(label='Логин пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


# ЭЛЕКТРОННАЯ ПОДПИСЬ
class Create_sig(forms.Form):
    file = forms.FileField(label='Документ')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class Check_sig(forms.Form):
    file = forms.FileField(label='Документ')
    signature = forms.FileField(label='Электронная подпись')
    user_tag = forms.CharField(label='Логин пользователя')


# АВТОРСТВО
class Create_author(forms.Form):
    file = forms.FileField(label='Документ')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class Check_author(forms.Form):
    file = forms.FileField(label='Документ')