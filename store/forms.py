from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import *


class BootstrapStylesMixin:
    form_fields = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.form_fields:
            for fieldname in self.form_fields:
                self.fields[fieldname].widget.attrs = {'class': 'form-control'}

        else:
            raise ValueError('The form_fields should be set')


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class OrderType(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order_type']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class MyPasswordChangeForm(BootstrapStylesMixin, PasswordChangeForm):
    form_fields = ['old_password', 'new_password1', 'new_password2']
