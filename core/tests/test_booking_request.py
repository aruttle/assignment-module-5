from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from glamp_messaging.models import Message

User = get_user_model()

class BookingRequestTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@example.com", full_name="Admin", password="Admin123!", is_staff=True
        )
        self.user = User.objects.create_user(
            email="guest@example.com", full_name="Guest", password="Guest123!"
        )

    def test_requires_login(self):
        resp = self.client.get(reverse("bookings:booking_request"))
        # Redirect to login
        self.assertEqual(resp.status_code, 302)

    def test_post_sends_message_to_admins(self):
        self.client.login(username="guest@example.com", password="Guest123!")
        start = (timezone.now().date() + timedelta(days=3)).strftime("%Y-%m-%d")
        end = (timezone.now().date() + timedelta(days=5)).strftime("%Y-%m-%d")

        resp = self.client.post(
            reverse("bookings:booking_request"),
            {
                "start_date": start,
                "end_date": end,
                "guests": 2,
                "notes": "Near the water if possible",
            },
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        # At least one message to an admin
        self.assertTrue(
            Message.objects.filter(
                sender=self.user, recipient__is_staff=True, subject__icontains="Booking request"
            ).exists()
        )
