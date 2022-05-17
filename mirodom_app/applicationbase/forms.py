from django import forms
from django.forms import ModelForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory


from .apps import user_registered

from .models import Appliactions, AdvUser, AdditionalImage

from captcha.fields import CaptchaField
from .models import Commet

class RegisterUserForm(forms.ModelForm):
    number = forms.CharField(required=True, label='Номер телефона')
    contract = forms.CharField(required=True, label='Введите номер договора')
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput, help_text='Повторите пароль')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            errors = {'password2':ValidationError(
                'Введенные пароли не совпадают', code='password_mismatch'
            )}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'contract', 'number',
                  'first_name', 'last_name', 'send_messages')




class AppForm (ModelForm):
    class Meta:
        model = Appliactions
        fields = ('master','city', 'address','flat','author','full_name_client', 'reason_for_calling','treaty','door_closer','img_door_closer', 'monetary','sum','premium','fine','choose_fine','comment','status')
        widgets = {'author': forms.HiddenInput}
AIFormSet = inlineformset_factory(Appliactions,AdditionalImage, fields='__all__')


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    contract = forms.CharField(max_length=20, label='Номер договора')
    number = forms.CharField(max_length=11, label='Номер телефона')

    class Meta:
        model = AdvUser
        fields = ('username','email', 'first_name', 'last_name', 'send_messages','contract')


class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=30, label='')

class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Commet
        exclude = ('is_active',)
        widgets = {'app':forms.HiddenInput}

class GuestCommentForm(forms.ModelForm):
    captcha = CaptchaField(label='Введите текст с картинки', error_messages={'invalid':'Неправильный текст'})
    class Meta:
        model = Commet
        exclude = ('is_active',)
        widgets = {'app':forms.HiddenInput}
