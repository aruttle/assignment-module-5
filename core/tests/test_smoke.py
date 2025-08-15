from django.test import TestCase
from django.urls import reverse

class SmokeTests(TestCase):
    def test_homepage_renders(self):
        resp = self.client.get(reverse("core:home"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Shannon")
