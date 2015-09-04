"""
AllNewsFeedReader class reads multiple RSS news feeds to populate the
Read All News page.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from threading import Thread
import queue
from collections import namedtuple
from .feed_reader import FeedReader

# TODO: Note the definition of the named tuple TypedNews.
# (no code change required)
TypedNews = namedtuple('TypedNews', 'news_type news')

""" TODO: You'll use TypedNews in the methods below. Example:
>>> news_type = 'concert'
>>> news = {'title': 'Best concert ever!'}
>>> typed_news = TypedNews(news_type, news)
>>> print(typed_news.news_type, 'news is', typed_news.news)
concert news is {'title': 'Best concert ever!'}
"""


class AllNewsFeedReader:
    """Reads news feeds for music, concerts, and sports"""

    # TODO: note the initialization of the `feed_reader` attribute
    # (no code change required)
    def __init__(self):
        self.feed_reader = FeedReader()

    # TODO: note that the get_news() method downloads news of all types.
    # (no code change required)
    def get_news(self, max_items=0):
        """
        Get news items of all news types.

        :param: max_items: if max_items > 0, return no more than max_items
        news items. Otherwise, return all news items.
        :return dictionary of news items.
        """

        # TODO: Note that the following code waits for each call to the
        # feed_reader's get_news() method to complete before calling the method
        # for the next news type.
        # You will improve the code's performance by creating a thread for each
        # news type so you can download all three news types concurrently.
        # all_news = {}
        # for news_type in 'concerts', 'sports', 'movies':
        #     news = self.feed_reader.get_news(news_type, max_items)
        #     all_news[news_type] = news
        # return all_news
        # TODO: comment out the 5 lines of code above this comment

        # TODO: create a Queue to hold the news from each thread. Assign
        # the Queue to a variable named `results_q`
        # HINT: see slide 9-30
        results_q = queue.Queue()

        # TODO: assign an empty list to the variable named `news_threads`.
        # The `news_threads` list will contain references to the Thread objects
        # that are downloading the news.
        news_threads = []

        for news_type in 'concerts', 'sports', 'movies':
            # TODO: Create a thread to download one type of news.
            # target: AllNewsFeedReader.worker (you'll write this method soon)
            # args: self, results_q, news_type, max_items
            # HINT: see slide 9-18
            background = Thread(target=AllNewsFeedReader.worker,
                                args=(self, results_q,
                                      news_type, max_items))

            # TODO: Append the new thread to the `news_threads` list
            news_threads.append(background)

            # TODO: Start the new thread
            # HINT: see slide 9-17
            background.start()

        # TODO: use a `for` loop to process each thread on the `news_threads`
        # list
        for thread in news_threads:
            # TODO: wait for the thread to complete by calling
            # the thread's join() method
            # HINT: see slide 9-17
            thread.join()

        # TODO: scroll to the definition of the method named `worker` below and
        # complete the TODO steps there.
        # When you are finished with `worker`, complete the remaining steps in
        # this method.

        # TODO: note the definition of the dictionary named `all_news`
        # (no code change required)
        all_news = {}

        # TODO: loop over `results_q`
        # HINT: see slide 9-31
        while not results_q.empty():
            # TODO: get the thread's result (a TypedNews object) from
            # `results_q` and assign it to a variable named `typed_news`
            typed_news = results_q.get_nowait()

            # TODO: add the data in `typed_news` to the `all_news` dictionary
            # key: the `news_type` attribute of `typed_news`
            # value: the `news` attribute of `typed_news`
            all_news[typed_news.news_type] = typed_news.news

        # TODO: return the `all_news` dictionary
        return all_news

    # TODO: note the parameters of the `worker` method.
    # (no code change required)
    def worker(self, results_q, news_type, max_items):
        """
        Download one type of news and add it to `results_q`.

        :param self: the current AllNewsFeedReader object
        :param results_q: a Queue of TypedNews instances
        :param news_type: a string with the type of news to download
        :param max_items: maximum number of news items to download
        """
        # TODO: use `self.feed_reader` to get news of the given `news_type` and
        # assign the result to a variable named `news`
        # HINT: this statement is exactly the same as a statement in the
        # original code that you commented out earlier.
        news = self.feed_reader.get_news(news_type, max_items)

        # TODO: create a TypedNews object and save the result in a local
        # variable.
        # HINT: see the definition of TypedNews at the beginning of this file.
        typed_news = TypedNews(news_type, news)

        # TODO: put the typed_news object on `results_q`
        results_q.put(typed_news)

        # To compare performance with the serial version of ticketmanor,
        # add a pause to this method:
        # import time; time.sleep(1)

        # TODO: complete the remaining steps in the get_news() method
