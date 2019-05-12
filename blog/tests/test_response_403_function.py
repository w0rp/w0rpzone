import unittest

from django.http import HttpRequest

from blog.views import response_403


class Response403TestCase(unittest.TestCase):
    def test_generic_403_response(self):
        request = HttpRequest()
        request.method = 'GET'

        response = response_403(request)
        self.assertEqual(response.status_code, 403)
        self.assertIn(b'<title>403: Forbiddena</title>', response.content)
        self.assertIn(b'<meta name="description" content="SOUTHERN CROSS!">', response.content)  # noqa
        self.assertIn(b'<iframe width="400" height="300" src="https://www.youtube.com/embed/e37Ri_5xY5U?autoplay=1" frameborder="0" allowfullscreen></iframe</iframe>', response.content)  # noqa
