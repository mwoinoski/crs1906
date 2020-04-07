"""
AllNewsFeedReader class reads multiple RSS news feeds to populate the
Read All News page.

This implementation stores the results of each news thread on a queue.Queue.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from threading import Thread
import queue

import concurrent.futures
from collections import namedtuple
from .feed_reader import FeedReader

# TODO: import ThreadPoolExecutor from concurrent.futures
from concurrent.futures import ThreadPoolExecutor

TypedNews = namedtuple('TypedNews', 'news_type news')


class AllNewsFeedReader:
    """Reads news feeds for music, concerts, and sports"""

    def __init__(self):
        self.feed_reader = FeedReader()

    def get_news(self, max_items=0):
        """Get news items of all news types."""

        results_q = queue.Queue()

        news_threads = []

        # TODO: wrap the `for` loop in a `with` statement that initializes
        #       a ThreadPoolExecutor. Pass the argument max_workers=4 to the
        #       ThreadPoolExecutor constructor.
        with ThreadPoolExecutor(max_workers=4) as executor:
            for news_type in 'concerts', 'sports', 'movies':
                # TODO: replace the call to the Thread constructor with a
                #       call to executor.submit().
                #       Arguments to submit: AllNewsFeedReader.worker, self,
                #                      results_q, news_type, max_items
                #       Assign the Future returned by submit to the variable
                #       `background`
                background = executor.submit(AllNewsFeedReader.worker, self,
                                             results_q, news_type, max_items)
                # background = Thread(target=AllNewsFeedReader.worker,
                #                     args=(self, results_q,
                #                           news_type, max_items))
                news_threads.append(background)

                # TODO: delete the call to background.start()
                # background.start()

        # TODO: in the following `for` statement, replace `news_threads` with
        #       a call to concurrent.futures.as_completed(news_threads)
        for thread in concurrent.futures.as_completed(news_threads):
        # for thread in news_threads:
            # TODO: replace the call to thread.join() with `pass`
            pass
            # thread.join()

        # TODO: note that the remainder of the code is unchanged.
        #       (no code changes required)

        all_news = {}

        while not results_q.empty():
            typed_news = results_q.get_nowait()
            all_news[typed_news.news_type] = typed_news.news

        return all_news

    def worker(self, results_q, news_type, max_items):
        """Download one type of news and add it to results_q."""
        news = self.feed_reader.fetch_news_items(news_type, max_items)
        typed_news = TypedNews(news_type, news)
        results_q.put(typed_news)
