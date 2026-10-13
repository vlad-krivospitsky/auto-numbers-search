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


class StaffAccessTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staffuser",
            email="staff@example.com",
            password="password123",
            is_staff=True,
        )
        self.regular_user = User.objects.create_user(
            username="regularuser",
            email="regular@example.com",
            password="password123",
            is_staff=False,
        )

    def test_unauthenticated_cannot_access_user_list(self):
        response = self.client.get(reverse("accounts:user_list"))
        self.assertEqual(response.status_code, 403)

    def test_regular_user_cannot_access_user_list(self):
        self.client.login(username="regularuser", password="password123")
        response = self.client.get(reverse("accounts:user_list"))
        self.assertEqual(response.status_code, 403)

    def test_staff_user_can_access_user_list(self):
        self.client.login(username="staffuser", password="password123")
        response = self.client.get(reverse("accounts:user_list"))
        self.assertEqual(response.status_code, 200)

    def test_staff_user_can_toggle_admin_role(self):
        self.client.login(username="staffuser", password="password123")
        response = self.client.post(
            reverse("accounts:toggle_admin", kwargs={"user_id": self.regular_user.id})
        )
        self.assertRedirects(response, reverse("accounts:user_list"))
        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.is_staff)

