from datetime import datetime

try:
    from urllib import request
except ImportError:
    import urllib2 as request

import xml.dom.minidom

from pysense.actions import notify
from pysense.thought import ThoughtBase
from pysense.memories import db, find_in_table, save_in_table

class FeedsThought(ThoughtBase):

    def run(self):
        pass

    def list(self, argv):
        feeds = []
        for feed in self.__table().all():
            feeds.append(feed['src'])

        return "\n".join(feeds)

    def add(self, argv):
        address = argv[3]
        feed_title = self.__get_feed_title(address)
        save_in_table(self.__table(), address, [])
        return feed_title

    def __table(self):
        return db().table('feeds')

    def __get_feed_title(self, address):
        content = request.urlopen(address).read()
        DOMTree = xml.dom.minidom.parseString(content)
        collection = DOMTree.documentElement
        return collection.getElementsByTagName('title')[0].firstChild.data

def init():
    thought = FeedsThought()
    thought.schedule(after=60)
    return thought

