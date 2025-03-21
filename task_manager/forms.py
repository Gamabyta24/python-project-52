from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label=_('First name'))
    last_name = forms.CharField(max_length=30, required=True, label=_('Last name'))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label=_('First name'))
    last_name = forms.CharField(max_length=30, required=True, label=_('Last name'))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Получаем текущий экземпляр пользователя, если он есть
        user_instance = getattr(self, 'instance', None)
        
        # Проверяем уникальность имени пользователя, исключая текущего пользователя
        if user_instance and User.objects.filter(username=username).exclude(pk=user_instance.pk).exists():
            raise forms.ValidationError(_('A user with that username already exists.'))
        # Если это создание нового пользователя, выполняем стандартную проверку
        elif not user_instance and User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('A user with that username already exists.'))
        
        return username