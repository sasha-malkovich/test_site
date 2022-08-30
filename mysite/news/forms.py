from django import forms
# from .models import Category
from .models import News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# описание формы связанной с моделью
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__' # будут представленны все поля из модели
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, }),
            'category': forms.Select(attrs={'class': 'form-control', }),
        }

    # hand-made validation
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Заголовок не должен начинаться с цифры')
        return title


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', help_text='help text', widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off', 'autofocus': 'none'}))
    email = forms.EmailField(label='Электронная почта',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # плюс еще может быть first_name, last_name
        # так как написано ниже сделать не получается, поэтому выше в классе самом будем переопределять каждое поле!
        #
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        # }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# описание формы не связанной с моделью
#
# class NewsForm(forms.Form):
#     title = forms.CharField(label='Заголовок', max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
#     content = forms.CharField(label='Текст', required=False, widget=forms.Textarea(attrs={
#         'class':'form-control',
#         'rows': 5,
#     }))
#     is_published = forms.BooleanField(label='Опубликовать', initial=True)
#     category = forms.ModelChoiceField(empty_label='Выбрать', label='Категория', queryset=Category.objects.all(),
#                                       widget=forms.Select(attrs={
#                                           'class': 'form-control',
#                                       }))
