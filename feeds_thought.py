from datetime import datetime

try:
    from urllib import request
except ImportError:
    import urllib2 as request

import xml.dom.minidom

from pysense.actions import notify
from pysense.thought import ThoughtBase
from pysense.memories import db, all, save_in_table

class FeedsThought(ThoughtBase):

    def run(self):
        table = self.__table()
        for feed in all(table):
            address = feed['name']
            feed_content = self.__get_feed_content(address)
            items = self.__notify_unread_items(feed_content, feed['value'])
        save_in_table(table, feed, items)

    def list(self, argv):
        feeds = []
        for feed in all(self.__table()):
            feeds.append(feed['name'])

        return "\n".join(feeds)

    def add(self, argv):
        address = argv[3]
        feed_content = self.__get_feed_content(address)
        feed_title = self.__get_feed_title(feed_content)
        save_in_table(self.__table(), address, [])
        return feed_title

    def __table(self):
        return db().table('feeds')

    def __get_feed_content(self, address):
        content = request.urlopen(address).read()
        DOMTree = xml.dom.minidom.parseString(content)
        collection = DOMTree.documentElement
        return collection

    def __get_feed_title(self, content):
        return content.getElementsByTagName('title')[0].firstChild.data

    def __notify_unread_items(self, content, items):
        title = self.__get_feed_title(content)
        for item in content.getElementsByTagName('item'):
            item_title = item.getElementsByTagName('title')[0].firstChild.data
            if not item_title in items:
                notify(title, item_title)
                items.append(item_title)
        return items

def init():
    thought = FeedsThought()
    thought.schedule(after=60)
    return thought

