from django.test import TestCase
from django.core.urlresolvers import reverse as url_reverse

TZ = "Europe/London"


class SettingsTestCase(TestCase):
    def test_load_settings_view(self):
        response = self.client.get(url_reverse("settings"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_post_timezone(self):
        url = url_reverse("settings")

        response = self.client.post(url, {"timezone": TZ})

        self.assertRedirects(response, url)

        self.assertIn("timezone", response.client.cookies)
        self.assertEqual(response.client.cookies["timezone"].value, TZ)

    def test_post_invalid_timezone(self):
        response = self.client.post(
            url_reverse("settings"),
            {"timezone": "xyz"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("timezone", response.context["form"].errors)

        self.assertNotIn("timezone", response.client.cookies)

    def test_post_valid_settings_ajax(self):
        response = self.client.post(
            url_reverse("settings"),
            {"timezone": TZ},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"{}")

        self.assertIn("timezone", response.client.cookies)
        self.assertEqual(response.client.cookies["timezone"].value, TZ)

    def test_post_invalid_timezone_ajax(self):
        response = self.client.post(
            url_reverse("settings"),
            {"timezone": "xyz"},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 400)

        self.assertNotIn("timezone", response.client.cookies)
