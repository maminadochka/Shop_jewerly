from django.forms import Form, ModelForm, TextInput, CharField, EmailInput, PasswordInput, ValidationError
from django.contrib.auth.models import User as DjangoUser


class LoginForm(Form):
    username = CharField(label="Username")
    password = CharField(label="Password", widget=PasswordInput())

    def clean(self):
        data = self.cleaned_data
        if 'username' not in data and 'password' not in data:
            raise ValidationError("Please enter correct data")
        return data


class UserForm(ModelForm):
    class Meta:
        model = DjangoUser
        fields = ['username', 'email', 'password']

    def clean_password(self):
        if self.data['password']:
            _user = DjangoUser()
            _user.set_password(self.data['password'])
            return _user.password
        else:
            raise ValidationError("Don't understand You")