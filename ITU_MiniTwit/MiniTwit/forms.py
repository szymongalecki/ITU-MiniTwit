from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("username", "email")

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # customize the form fields, add extra widgets etc.

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:

            # Get the user with username 'myusername'
            try:
                user1 = User.objects.get(username=username)
            except User.DoesNotExist:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            if(check_password_hash(user1.password, password)):
                user = user1
            else:
                pwd = generate_password_hash(password)
                user = authenticate(username=username, password=pwd)
            if user is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.user_cache = user
        return self.cleaned_data