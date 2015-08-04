"""
Unit tests for AtomNewsFeedParser class.
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

from unittest import TestCase, main
from ticketmanor.rest_services.feed_reader.atom_news_feed_parser import AtomNewsFeedParser


class TestAtomNewsFeedParser(TestCase):
    """Unit tests for AtomNewsFeedParser"""

    def test_get_news_music(self):
        feed_reader = AtomNewsFeedParser()

        result = feed_reader.parse_content(parse_content_input)

        for i, news_item in enumerate(result, start=0):
            self.assertTrue(parse_content_results[i]['title'],
                            news_item['title'])
            self.assertTrue(parse_content_results[i]['date_time'],
                            news_item['date_time'])
            self.assertTrue(parse_content_results[i]['image_thumbnail'],
                            news_item['image_thumbnail'])
            self.assertTrue(parse_content_results[i]['image_banner'],
                            news_item['image_banner'])
            self.assertTrue(parse_content_results[i]['content'],
                            news_item['content'])
        self.assertEqual(2, i)

    def test_get_news_max_items_1(self):
        feed_reader = AtomNewsFeedParser()

        result = feed_reader.parse_content(parse_content_input, max_items=1)

        for i, news_item in enumerate(result, start=0):
            self.assertTrue(parse_content_results[i]['title'],
                            news_item['title'])
            self.assertTrue(parse_content_results[i]['date_time'],
                            news_item['date_time'])
            self.assertTrue(parse_content_results[i]['image_thumbnail'],
                            news_item['image_thumbnail'])
            self.assertTrue(parse_content_results[i]['image_banner'],
                            news_item['image_banner'])
            self.assertTrue(parse_content_results[i]['content'],
                            news_item['content'])
        self.assertEqual(0, i)

    def test_get_news_max_items_2(self):
        feed_reader = AtomNewsFeedParser()

        result = feed_reader.parse_content(parse_content_input, max_items=2)

        for i, news_item in enumerate(result, start=0):
            self.assertTrue(parse_content_results[i]['title'],
                            news_item['title'])
            self.assertTrue(parse_content_results[i]['date_time'],
                            news_item['date_time'])
            self.assertTrue(parse_content_results[i]['image_thumbnail'],
                            news_item['image_thumbnail'])
            self.assertTrue(parse_content_results[i]['image_banner'],
                            news_item['image_banner'])
            self.assertTrue(parse_content_results[i]['content'],
                            news_item['content'])
        self.assertEqual(1, i)

# TODO: convert to AtomPub format
parse_content_input = \
    '<rss>' \
        '<item>' \
            '<title>The Othello of Soul Music - Wall Street Journal</title>' \
            '<pubDate>Fri, 29 May 2015 18:14:00 GMT</pubDate>' \
            '<description>' \
                '&lt;img src="https://t0.gstatic.com/images?q=tbn:...&gt;' \
                '&lt;div class="lh"&gt;&lt;br&gt;&lt;br&gt;&lt;font&gt;' \
                'Otis Redding is the Othello of soul &lt;b&gt;music&lt;/b&gt;' \
                '...&lt;/font&gt;' \
            '</description>' \
        '</item>' \
        '<item>' \
            '<title>Second Item</title>' \
            '<pubDate>Fri, 29 May 2015 19:25:00 GMT</pubDate>' \
            '<description>' \
                '&lt;img src="https://t0.gstatic.com/images?q=tbn:...&gt;' \
                '&lt;div class="lh"&gt;&lt;br&gt;&lt;br&gt;&lt;font&gt;' \
                'Second item content...&lt;/font&gt;' \
            '</description>' \
        '</item>' \
        '<item>' \
            '<title>Third Item</title>' \
            '<pubDate>Fri, 29 May 2015 20:36:00 GMT</pubDate>' \
            '<description>' \
                '&lt;img src="https://t0.gstatic.com/images?q=tbn:...&gt;' \
                '&lt;div class="lh"&gt;&lt;br&gt;&lt;br&gt;&lt;font&gt;' \
                'Third item content...&lt;/font&gt;' \
            '</description>' \
        '</item>' \
    '</rss>'

parse_content_results = [
    {'title': 'The Othello of Soul Music - Wall Street Journal',
     'date_time': 'Fri, 29 May 2015 18:14:00 GMT',
     'image_thumbnail': 'https://t0.gstatic.com/images?q=tbn:...',
     'image_banner': 'https://t0.gstatic.com/images?q=tbn:...',
     'content': 'Otis Redding is the Othello of soul music...'},
    {'title': 'Second Item',
     'date_time': 'Fri, 29 May 2015 19:25:00 GMT',
     'image_thumbnail': 'https://t0.gstatic.com/images?q=tbn:...',
     'image_banner': 'https://t0.gstatic.com/images?q=tbn:...',
     'content': 'Second item content...'},
    {'title': 'Third Item',
     'date_time': 'Fri, 29 May 2015 20:36:00 GMT',
     'image_thumbnail': 'https://t0.gstatic.com/images?q=tbn:...',
     'image_banner': 'https://t0.gstatic.com/images?q=tbn:...',
     'content': 'Third item content...'},
]

if __name__ == '__main__':
    main()
