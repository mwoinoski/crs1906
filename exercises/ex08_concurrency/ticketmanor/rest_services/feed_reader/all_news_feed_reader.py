"""
AllNewsFeedReader class reads multiple RSS news feeds to populate the
Read All News page.
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from threading import Thread
from .feed_reader import FeedReader


# TODO: make the NewsThread class a subclass of Thread
# HINT: see slide 8-11
class NewsThread(....):

    # TODO: note the arguments to the NewsThread constructor
    #       (no code change required)
    def __init__(self, feed_reader, news_type, max_items):
        """Initialize a NewsThread.

        :param feed_reader a FeedReader instance
        :param news_type: a string with the type of news to download
        :param max_items: maximum number of news items to download
        """
        super().__init__()
        # TODO: note that `self.feed_reader` is an instance of FeedReader
        #       (no code change required)
        self.feed_reader = feed_reader
        self.news_type = news_type
        self.max_items = max_items
        self.news = None

    # TODO: define a run() method that overloads the superclass run() method.
    def ....
        """Download one type of news and store it in self.news"""

        # TODO: use `self.feed_reader` to fetch news of the given
        #       `news_type` and assign the result to `self.news`
        ....


class AllNewsFeedReader:
    """Reads news feeds for music, concerts, and sports"""

    # TODO: note the initialization of the `feed_reader` attribute
    #       (no code change required)
    def __init__(self):
        self.feed_reader = FeedReader()

    # TODO: note that the get_news() method downloads news of all types.
    #       (no code change required)
    def get_news(self, max_items=0):
        """Get news items of all news types.

        :param: max_items: if max_items > 0, return no more than max_items
        news items. Otherwise, return all news items.
        :return dictionary of news items.
        """
        # TODO: assign an empty list to the variable named `news_threads`.
        #       The `news_threads` list will contain references to NewsThread
        #       instances that are downloading the news.
        news_threads = ....

        for news_type in 'concerts', 'sports', 'movies':
            # TODO: Create an instance of NewsThread to download one type of news.
            #       Constructor arguments: self.feed_reader, news_type, max_items
            # HINT: see slide 8-11
            ....

            # TODO: Append the new thread to the `news_threads` list
            ....

            # TODO: Start the new thread
            ....

        # TODO: note the definition of the dictionary named `all_news`
        #       (no code change required)
        all_news = {}

        # TODO: use a `for` loop to process each thread on the `news_threads`
        #       list
        ....
            # TODO: wait for the child thread to complete by calling
            #       the thread's join() method
            ....

            # TODO: Add the thread's news to the `all_news` dictionary.
            #       key: the thread's `news_type` attribute
            #       value: the thread's `news` attribute
            ....

        # TODO: return the `all_news` dictionary
        return ....
