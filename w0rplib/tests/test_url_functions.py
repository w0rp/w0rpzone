import unittest

from w0rplib.url import redir, redir_temp
from django.urls.resolvers import URLPattern
from django.http import HttpRequest


class URLFunctionTestCase(unittest.TestCase):
    def test_301_redirect(self):
        url_object = redir(r"^page/0*1/$", "/blog", name='blog-redir')

        self.assertIsInstance(url_object, URLPattern)
        self.assertEqual(url_object.name, 'blog-redir')
        self.assertEqual(url_object.pattern.regex.pattern, '^page/0*1/$')

        request = HttpRequest()
        request.method = 'GET'

        response = url_object.callback(request)

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], '/blog')

    def test_303_redirect(self):
        url_object = redir_temp(r"^page/0*1/$", "/blog", name='blog-redir')

        self.assertIsInstance(url_object, URLPattern)
        self.assertEqual(url_object.name, 'blog-redir')
        self.assertEqual(url_object.pattern.regex.pattern, '^page/0*1/$')

        request = HttpRequest()
        request.method = 'GET'

        response = url_object.callback(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/blog')
