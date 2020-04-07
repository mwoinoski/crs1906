"""
worker.py - FIXME
"""

import logging
from collections import namedtuple
# TODO: Note the definition of the named tuple TypedNews.
#       (no code change required)
TypedNews = namedtuple('TypedNews', 'news_type news')

logger = logging.getLogger(__name__)


# TODO: note the parameters of the `worker` method.
#       (no code change required)
def worker(feed_reader, results_q, news_type, max_items):
    """
    Download one type of news and add it to `results_q`.

    :param self: the current AllNewsFeedReader object
    :param results_q: a Queue of TypedNews instances
    :param news_type: a string with the type of news to download
    :param max_items: maximum number of news items to download
    """
    logger.debug("worker called for %s", news_type)

    # TODO: use `self.feed_reader` to get news of the given `news_type` and
    #       assign the result to a variable named `news`
    # HINT: this statement is exactly the same as a statement in the
    # original code that you commented out earlier.
    news = feed_reader.fetch_news_items(news_type, max_items)

    # TODO: create a TypedNews object and save the result in a local
    #       variable.
    # HINT: see the definition of TypedNews at the beginning of this file.
    typed_news = TypedNews(news_type, news)

    # TODO: put the typed_news object on `results_q`
    results_q.put(typed_news)
    return
    # To compare performance with the serial version of ticketmanor,
    # add a pause to this method:
    # import time; time.sleep(1)

    # TODO: complete the remaining steps in the get_news() method




