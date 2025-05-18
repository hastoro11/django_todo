from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username'
    }), label='')
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Login'))


class TODOForm(forms.Form):
    title = forms.CharField(max_length=128, label='', widget=forms.TextInput(attrs={
        'placeholder': 'Add new task',
        'class': 'form-control'
    }))