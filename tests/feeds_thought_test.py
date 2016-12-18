import unittest
from os.path import join, dirname
from unittest.mock import patch

from feeds_thought import FeedsThought

class FeedsThoughtTest(unittest.TestCase):

    def setUp(self):
        self.argv = ['think', 'feeds']

    @patch('feeds_thought.db')
    def test_list(self, table):
        class TableMocked:
            def all(self):
                return [
                    {'src': 'http://address.com/feed'}
                ]
        class DbMocked:
            def table(self, table):
                return TableMocked()
        table.return_value = DbMocked()
        t = FeedsThought()
        self.argv.append('list')
        self.assertEquals("http://address.com/feed", t.list(self.argv))

    @patch('feeds_thought.save_in_table')
    @patch('feeds_thought.request')
    def test_add(self, request, save_in_table):
        self.argv.append('add')
        self.argv.append('http://address.com/feed')

        def urlopen(address):
            fixture = join(dirname(__file__), 'fixtures', 'atom.xml')
            return open(fixture)
        request.urlopen = urlopen
        t = FeedsThought()
        self.assertEquals("Address' Feed", t.add(self.argv))

