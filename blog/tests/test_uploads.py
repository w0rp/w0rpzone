import json
from io import BytesIO
from unittest import mock

from django.core.files.base import File
from django.core.files.storage import FileSystemStorage
from django.test import TestCase
from django.urls import reverse as url_reverse

from .util import create_author


class UploadTestCase(TestCase):
    def test_get_response_as_anonymous_user(self):
        response = self.client.get(url_reverse('upload-file'))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b'{}')

    def test_post_response_as_anonymous_user(self):
        response = self.client.post(url_reverse('upload-file'))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b'{}')

    def test_get_response_as_authenticated_user(self):
        author = create_author()
        self.client.login(username=author.username, password="lolwat")

        response = self.client.get(url_reverse('upload-file'))

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.content, b'{}')

    def test_post_without_file(self):
        author = create_author()
        self.client.login(username=author.username, password="lolwat")

        response = self.client.post(url_reverse('upload-file'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'{}')

    @mock.patch.object(FileSystemStorage, 'url')
    @mock.patch.object(FileSystemStorage, 'save')
    def test_post_valid_file(self, save_mock, url_mock):
        author = create_author()
        self.client.login(username=author.username, password="lolwat")

        upload = {'filename': None, 'data': None}

        def save_side_effect(filename, file_obj):
            upload['filename'] = filename
            upload['data'] = file_obj.read()

            return 'New Filename'

        save_mock.side_effect = save_side_effect
        url_mock.return_value = '/media/foobar'

        response = self.client.post(url_reverse('upload-file'), {
            'file': File(BytesIO(b'123'), 'My Filename'),
        })

        self.assertEqual(response.status_code, 201)

        self.assertEqual(save_mock.call_count, 1)
        self.assertEqual(upload['filename'], 'My Filename')
        self.assertEqual(upload['data'], b'123')

        self.assertEqual(url_mock.call_count, 1)
        self.assertEqual(url_mock.call_args, mock.call('New Filename'))

        self.assertEqual(
            response.content,
            json.dumps({"url": "/media/foobar"}).encode('utf-8'),
        )
