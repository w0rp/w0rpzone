import unittest

from w0rplib.compiler import CSSCompressor, RJSMinCompressor


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
