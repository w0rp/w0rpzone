import unittest

from w0rplib.templatetags.text_formatting import word_break_on
from w0rplib.compiler import CSSCompressor, RJSMinCompressor


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


class CompilerTestCase(unittest.TestCase):
    def test_js_min(self):
        test_js = """
        function foo(x) {
            return x * 3;
        }
        """

        self.assertEqual(
            RJSMinCompressor(verbose=False).compress_js(test_js),
            "function foo(x){return x*3;}"
        )

    def test_css_min(self):
        test_css = """
        body {
            background: white;
        }
        """

        self.assertEqual(
            CSSCompressor(verbose=False).compress_css(test_css),
            "body{background:white}",
        )
