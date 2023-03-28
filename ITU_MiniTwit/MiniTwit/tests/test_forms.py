from django.test import TestCase
from MiniTwit.forms import CustomUserCreationForm, CustomUserChangeForm

class UserCreationFormTest(TestCase):

    def test_form(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password1': 'test123!',
            'password2': 'test123!',
        }

        form = CustomUserCreationForm(data)
        self.assertTrue(False)
        self.assertTrue(form.is_valid())

class UserChangeFormTest(TestCase):

    def test_form(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password1': 'test123!',
            'password2': 'test123!',
        }

        form = CustomUserChangeForm(data)

        self.assertTrue(form.is_valid())