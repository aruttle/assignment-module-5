
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve, resolve as _resolve
from django.shortcuts import resolve_url

User = get_user_model()

class ProjectsPermissionTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            email="staff@example.com", full_name="Staff", password="Staff123!", is_staff=True
        )
        self.user = User.objects.create_user(
            email="user@example.com", full_name="User", password="User123!"
        )

    def test_non_staff_redirects_or_403(self):
        """
        Our current view redirects non-staff to Home (/) instead of a login page.
        Accept 403 or 302; and if 302, allow either login or home as target.
        """
        self.client.login(username="user@example.com", password="User123!")
        resp = self.client.get(reverse("projects:project_list"))
        self.assertIn(resp.status_code, (302, 403), msg=f"Unexpected status: {resp.status_code}")

        if resp.status_code == 302:
            loc = resp["Location"]
            home_url = resolve_url("core:home")
            self.assertTrue(
                ("login" in loc.lower()) or (loc == "/" or loc == home_url),
                msg=f"Unexpected redirect target: {loc}",
            )

    def test_staff_ok(self):
        self.client.login(username="staff@example.com", password="Staff123!")
        resp = self.client.get(reverse("projects:project_list"))
        self.assertEqual(resp.status_code, 200)
