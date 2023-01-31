from django.test import TestCase
from django.urls import reverse_lazy

from users.models import EmailVerification, User


class UserRegistrationViewTest(TestCase):
    def setUp(self):
        self.path = reverse_lazy("users:register")
        self.data = {
            "first_name": "Никита",
            "last_name": "Полетаев",
            "username": "testname",
            "email": "test@mail.ru",
            "password1": "12345678Dj",
            "password2": "12345678Dj",
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/registration.html")
        self.assertEqual(response.context_data["title"], "Регистрация")

    def test_user_registration_post_success(self):

        username = self.data["username"]
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, self.data)
        # Проверка регистрации пользователя
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users:login"))
        self.assertTrue(User.objects.filter(username=username).exists())

        # Проверка подтверждения почты
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())

    def test_user_registration_post_error(self):
        user = User.objects.create(username=self.data["username"])
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Пользователь с таким именем уже существует.", html=True
        )
