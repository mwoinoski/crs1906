"""
Unit tests for util functions
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from unittest import TestCase

from ticketmanor.util.utils import html_escape, html_unescape


class TestUtil(TestCase):
    """Unit tests for utility functions"""

    def test_html_escape(self):
        html = html_escape(TestUtil.unescaped_html)
        self.assertEqual(TestUtil.escaped_html, html)

    def test_html_unescape(self):
        html = html_unescape(TestUtil.escaped_html)
        self.assertEqual(TestUtil.unescaped_html, html)

    def test_html_unescape_no_double_unescape(self):
        orginal = "&amp;lt;br&amp;gt;"
        html = html_unescape(orginal)
        self.assertEqual("&lt;br&gt;", html)

    unescaped_html = """
        <table border="0" cellpadding="2" cellspacing="7"
        style="vertical-align:top;">
        <tr><td width="80" align="center" valign="top">
        "Some" 'text'</td></tr>
        <tr><td width="80" align="center" valign="top">
        <img src='http://site?x=1&y=2&z=3</td></tr>
        </table>
    """

    escaped_html = """
        &lt;table border=&quot;0&quot; cellpadding=&quot;2&quot; cellspacing=&quot;7&quot;
        style=&quot;vertical-align:top;&quot;&gt;
        &lt;tr&gt;&lt;td width=&quot;80&quot; align=&quot;center&quot; valign=&quot;top&quot;&gt;
        &quot;Some&quot; &apos;text&apos;&lt;/td&gt;&lt;/tr&gt;
        &lt;tr&gt;&lt;td width=&quot;80&quot; align=&quot;center&quot; valign=&quot;top&quot;&gt;
        &lt;img src=&apos;http://site?x=1&amp;y=2&amp;z=3&lt;/td&gt;&lt;/tr&gt;
        &lt;/table&gt;
    """
