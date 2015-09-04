"""
AllNewsFeedReader class reads multiple RSS news feeds to populate the
Read All News page.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from threading import Thread
import queue

from collections import namedtuple
from .feed_reader import FeedReader

TypedNews = namedtuple('TypedNews', 'news_type news')


class AllNewsFeedReader:
    """Reads news feeds for music, concerts, and sports"""

    def __init__(self):
        self.feed_reader = FeedReader()

    def get_news(self, max_items=0):
        """
        Get news items of all news types.

        :param: max_items: if max_items > 0, return no more than max_items
        news items. Otherwise, return all news items.
        :return dictionary of news items.
        """
        results_q = queue.Queue()

        news_threads = []
        for news_type in 'concerts', 'sports', 'movies':
            background = Thread(target=AllNewsFeedReader.worker,
                                 args=(self, results_q,
                                       news_type, max_items))
            news_threads.append(background)
            background.start()

        for thread in news_threads:
            thread.join()

        all_news = {}

        while not results_q.empty():
            typed_news = results_q.get_nowait()
            all_news[typed_news.news_type] = typed_news.news

        return all_news

    def worker(self, results_q, news_type, max_items):
        """
        Download one type of news and add it to results_q.

        :param self: the current AllNewsFeedReader object
        :param results_q: a Queue of TypedNews instances
        :param news_type: a string with the type of news to download
        :param max_items: maximum number of news items to download
        """
        news = self.feed_reader.get_news(news_type, max_items)
        typed_news = TypedNews(news_type, news)
        results_q.put(typed_news)
