import textwrap
import unittest

from w0rplib.templatetags.markdown import markdown, unsafe_markdown


class MarkdownTestCase(unittest.TestCase):
    def test_html_escaping(self):
        # This value was used to demonstrate a flaw with the markdown2 library.
        text = '<<svg/onload=prompt(1) x'

        self.assertEqual(
            unsafe_markdown(text),
            '<p>&lt;<svg/onload=prompt(1) x</p>\n',
        )
        self.assertEqual(
            markdown(text),
            '<p>&lt;&lt;svg/onload=prompt(1) x&lt;/p&gt;'
            + '\n</p>'
        )

    def test_ordered_list_formatting(self):
        text = textwrap.dedent(r'''
        1. foo
        2. bar
        3. baz
        ''')
        html = textwrap.dedent(r'''
        <ol>
        <li>foo</li>
        <li>bar</li>
        <li>baz</li>
        </ol>
        ''').lstrip()

        self.assertEqual(unsafe_markdown(text), html)
        self.assertEqual(markdown(text), html)

    def test_unordered_list_formatting(self):
        text = textwrap.dedent(r'''
        * foo
        * bar
        * baz
        ''')
        html = textwrap.dedent(r'''
        <ul>
        <li>foo</li>
        <li>bar</li>
        <li>baz</li>
        </ul>
        ''').lstrip()

        self.assertEqual(unsafe_markdown(text), html)
        self.assertEqual(markdown(text), html)

    def test_emphasis(self):
        text = '_foo_ __bar__ *foo* **bar**'
        html = '<p>_foo_ __bar__ <em>foo</em> <strong>bar</strong></p>\n'

        self.assertEqual(unsafe_markdown(text), html)
        self.assertEqual(markdown(text), html)

    def test_links(self):
        text = '[foo](https://bar.com)'
        html = '<p><a href="https://bar.com">foo</a></p>\n'

        self.assertEqual(unsafe_markdown(text), html)
        self.assertEqual(markdown(text), html)

    def test_language_for_highlights_with_markdown_tags(self):
        text = textwrap.dedent(r"""
        ```js
        const x = 1
        ```
        """)
        html = '<pre><code class="js">const x = 1\n</code></pre>\n'

        self.assertEqual(unsafe_markdown(text), html)
        self.assertEqual(markdown(text), html)

    def test_table_formatting(self):
        text = textwrap.dedent(r"""
        heading 1 | heading 2
        ----------|----------
        col 1     | col 2
        col 1     | col 2
        """)
        html = textwrap.dedent(r"""
        <table>
        <thead>
        <tr>
          <th>heading 1</th>
          <th>heading 2</th>
        </tr>
        </thead>
        <tbody>
        <tr>
          <td>col 1</td>
          <td>col 2</td>
        </tr>
        <tr>
          <td>col 1</td>
          <td>col 2</td>
        </tr>
        </tbody>
        </table>
        """).strip() + "\n"

        self.assertEqual(unsafe_markdown(text), html)
        self.assertEqual(markdown(text), html)
