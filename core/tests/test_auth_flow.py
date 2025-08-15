from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

User = get_user_model()

class AuthFlowTests(TestCase):
    def test_register_login_cycle(self):
        # Register
        resp = self.client.post(
            reverse("users:register"),
            {
                "email": "test@example.com",
                "full_name": "Test User",
                "password1": "SuperStrongPass123!",
                "password2": "SuperStrongPass123!",
            },
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

        # Login
        resp = self.client.post(
            reverse("users:login"),
            {"username": "test@example.com", "password": "SuperStrongPass123!"},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.wsgi_request.user.is_authenticated)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_password_reset_sends_email(self):
        User.objects.create_user(
            email="reset@example.com",
            full_name="Reset User",
            password="Pass12345!"
        )
        resp = self.client.post(
            reverse("users:password_reset"),
            {"email": "reset@example.com"},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)

        from django.core import mail
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("reset@example.com", mail.outbox[0].to)
