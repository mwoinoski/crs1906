"""
AllNewsFeedReader class reads multiple RSS news feeds to populate the
Read All News page.
"""

import concurrent.futures
from .feed_reader import FeedReader

# TODO: import ThreadPoolExecutor from concurrent.futures
from concurrent.futures import ThreadPoolExecutor

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'


# TODO: note the definition of the NewsReader class. NewsReader.get_news()
# will download one type of news.
# Also note that this is not a Thread subclass.
# (no code change required)
class NewsReader:
    # TODO: note the arguments to the NewsReader constructor
    # (no code change required)
    def __init__(self, feed_reader, news_type, max_items):
        """Initialize a NewsThread"""
        self.feed_reader = feed_reader
        self.news_type = news_type
        self.max_items = max_items
        self.news = None

    # TODO: note the definition of the get_news() method
    # (no code change required)
    def get_news(self):
        """Download one type of news and store it in self.news"""
        self.news = self.feed_reader.fetch_news_items(self.news_type,
                                                      self.max_items)
        # TODO: note this method returns a reference to the current NewsReader
        # (no code change required)
        return self


class AllNewsFeedReader:
    """Reads news feeds for music, concerts, and sports"""

    def __init__(self):
        self.feed_reader = FeedReader()

    def get_news(self, max_items=0):
        """Get news items of all news types."""

        # TODO: assign an empty list to the variable `news_futures`
        news_futures = []

        # TODO: wrap the `for` loop in a `with` statement that initializes
        # a ThreadPoolExecutor. Pass the argument max_workers=4 to the
        # ThreadPoolExecutor constructor.
        # HINT: see slide 9-43
        with ThreadPoolExecutor(max_workers=4) as executor:
            for news_type in 'concerts', 'sports', 'movies':

                # TODO: create an instance of NewsReader and assign it to a
                # local variable named `news_reader`
                news_reader = NewsReader(self.feed_reader, news_type, max_items)

                # TODO: call executor.submit() to execute the NewsReader's
                # get_news() method.
                # Arguments to submit: NewsReader.get_news, news_reader
                # Assign the Future returned by submit to a local variable.
                future = executor.submit(NewsReader.get_news, news_reader)

                # TODO: append the Future to the `news_futures` list
                news_futures.append(future)

        # TODO: initialize the `all_news` variable with an empty dictionary
        # (no code change required)
        all_news = {}

        # TODO: use a `for` to loop over the result of a call to
        # concurrent.futures.as_completed(news_futures)
        # HINT: see slide 9-47
        for future in concurrent.futures.as_completed(news_futures):

            # TODO: assign the result of the Future to a variable named
            # `news_reader`
            news_reader = future.result()

            # TODO: note that the result of the Future is the result of the
            # NewReader's get_news() method, which returns a reference to the
            # current NewsReader.
            # (no code change required)

            # TODO: Add the NewsReader's news to the `all_news` dictionary.
            # key: the news_reader's `news_type` attribute
            # value: the news_reader's `news` attribute
            all_news[news_reader.news_type] = news_reader.news

        # TODO: return the `all_news` dictionary
        return all_news
