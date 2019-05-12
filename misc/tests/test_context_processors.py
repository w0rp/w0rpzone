from collections import namedtuple
from unittest import TestCase

from misc.context_processors import navigation

FakeRequest = namedtuple("FakeRequest", "path")


class ContextProcessorTestCase(TestCase):
    def test_navigation_processor_for_blog(self):
        self.assertEqual(navigation(FakeRequest("/blog")), {
            "main_nav": "blog",
        })

    def test_navigation_processor_for_other_locations(self):
        self.assertEqual(navigation(FakeRequest("/other")), {
            "main_nav": "",
        })
