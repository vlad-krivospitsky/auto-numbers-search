from django.test import TestCase
from django.urls import reverse
from apps.accounts.forms import CustomUserCreationForm
from apps.accounts.models import User


class AccountsRegistrationTests(TestCase):
    def test_form_has_no_help_texts(self):
        form = CustomUserCreationForm()
        for name, field in form.fields.items():
            self.assertIsNone(field.help_text, f"Field {name} should have no help_text")

    def test_signup_with_4_char_password_success(self):
        data = {
            "username": "user4char",
            "email": "user4@example.com",
            "password1": "1234",
            "password2": "1234",
        }
        response = self.client.post(reverse("accounts:signup"), data)
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertTrue(User.objects.filter(username="user4char").exists())

    def test_signup_with_short_password_fails(self):
        data = {
            "username": "user3char",
            "email": "user3@example.com",
            "password1": "123",
            "password2": "123",
        }
        response = self.client.post(reverse("accounts:signup"), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="user3char").exists())
