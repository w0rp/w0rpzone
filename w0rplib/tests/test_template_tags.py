import unittest

from w0rplib.templatetags.text_formatting import word_break_on


class TemplateTagTestCase(unittest.TestCase):
    def test_word_break_on(self):
        self.assertEqual(
            word_break_on("foo.bar.baz", "."),
            "foo.<wbr>bar.<wbr>baz"
        )

    def test_word_break_on_escapes_html(self):
        self.assertEqual(
            word_break_on("foo.bar<script>", "."),
            "foo.<wbr>bar&lt;script&gt;"
        )
