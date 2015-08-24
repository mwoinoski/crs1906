"""
all_news_feed_reader.py - reads multiple RSS news feeds to populate the
Read All News page.
"""
from threading import Thread

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

import queue
from .feed_reader import (
    FeedReader,
)


class AllNewsFeedReader:
    """Reads news feeds for music, concerts, and sports"""
    def __init__(self):
        self.feed_reader = FeedReader()

    def get_news(self, max_items=0):
        """
        Get news items of all news types.

        If max_items > 0, return no more than max_items news items.
        Otherwise, return all news items.
        """
        results_q = queue.Queue()

        # start a thread for each news type and add the thread to a list
        news_threads = []
        for news_type in 'music', 'sports', 'movies':
            thread = Thread(target=AllNewsFeedReader.worker,
                            args=(self.feed_reader, results_q,
                                  news_type, max_items))
            news_threads.append()
            thread.start()

        # wait for all threads in the list to complete
        for thread in news_threads:
            thread.join()

        # add each item on result queue to a dictionary
        all_news = {}
        while not results_q.empty():
            news_type, news = results_q.get()
            all_news[news_type] = news

        return all_news

        # music_news = self.feed_reader.fetch_news_items('music', max_items)
        # sports_news = self.feed_reader.fetch_news_items('sports', max_items)
        # movie_news = self.feed_reader.fetch_news_items('movies', max_items)
        # return {'music': music_news, 'sports': sports_news, 'movie': movie_news}

    def worker(self, results, news_type, max_items):
        news = self.feed_reader.get_news(news_type, max_items)
        results.put((news_type, news))
