from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from glamp_messaging.models import Message

User = get_user_model()

class InboxAndSendTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@example.com", full_name="Admin", password="Admin123!", is_staff=True
        )
        self.alice = User.objects.create_user(
            email="alice@example.com", full_name="Alice", password="Alice123!"
        )
        self.bob = User.objects.create_user(
            email="bob@example.com", full_name="Bob", password="Bob123!"
        )

        # Messages to Alice (recipient)
        Message.objects.create(sender=self.admin, recipient=self.alice, subject="Active 1", body="x", archived=False)
        Message.objects.create(sender=self.admin, recipient=self.alice, subject="Archived 1", body="y", archived=True)

    def test_inbox_active_vs_archived(self):
        self.client.login(username="alice@example.com", password="Alice123!")

        # Active (default)
        resp = self.client.get(reverse("glamp_messaging:inbox"))
        self.assertEqual(resp.status_code, 200)
        qs = resp.context["messages_qs"]
        self.assertTrue(all(m.archived is False for m in qs))

        # Archived via ?filter=archived
        resp = self.client.get(reverse("glamp_messaging:inbox") + "?filter=archived")
        self.assertEqual(resp.status_code, 200)
        qs = resp.context["messages_qs"]
        self.assertTrue(all(m.archived is True for m in qs))

        # Archived via legacy ?status=archived
        resp = self.client.get(reverse("glamp_messaging:inbox") + "?status=archived")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(all(m.archived is True for m in resp.context["messages_qs"]))

        # Archived via legacy ?archived=1
        resp = self.client.get(reverse("glamp_messaging:inbox") + "?archived=1")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(all(m.archived is True for m in resp.context["messages_qs"]))

    def test_non_admin_cannot_message_non_admin(self):
        """
        Non-staff users see only admins in the recipient field.
        Posting a non-admin recipient triggers Django's default
        'Select a valid choice...' error, or our custom message
        if validation reaches the view-level check.
        """
        self.client.login(username="alice@example.com", password="Alice123!")
        resp = self.client.post(
            reverse("glamp_messaging:send_message"),
            {"recipient": self.bob.id, "subject": "Hi", "body": "Hello"},
        )
       
        self.assertEqual(resp.status_code, 200)

        
        self.assertFalse(Message.objects.filter(sender=self.alice, recipient=self.bob, subject="Hi").exists())

        content = resp.content.decode()
        self.assertTrue(
            ("Select a valid choice." in content)
            or ("You can only message site administrators." in content),
            msg="Expected either the default invalid-choice error or the custom admin-only message.",
        )

    def test_non_admin_can_message_admin(self):
        self.client.login(username="alice@example.com", password="Alice123!")
        resp = self.client.post(
            reverse("glamp_messaging:send_message"),
            {"recipient": self.admin.id, "subject": "Hi", "body": "Hello"},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Message.objects.filter(sender=self.alice, recipient=self.admin, subject="Hi").exists())
