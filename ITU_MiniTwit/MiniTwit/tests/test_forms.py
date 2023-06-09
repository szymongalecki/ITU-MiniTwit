from django.test import TestCase
from MiniTwit.forms import CustomUserCreationForm, CustomUserChangeForm
import os

test_password = os.environ.get("TEST_PASSWORD")

class UserCreationFormTest(TestCase):

    def test_form(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password1': test_password,
            'password2': test_password,
        }

        form = CustomUserCreationForm(data)

        self.assertTrue(form.is_valid())

class UserChangeFormTest(TestCase):

    def test_form(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password1': test_password,
            'password2': test_password,
        }

        form = CustomUserChangeForm(data)

        self.assertTrue(form.is_valid())