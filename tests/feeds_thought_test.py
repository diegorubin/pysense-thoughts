import unittest
from os.path import join, dirname
from unittest.mock import patch

from feeds_thought import FeedsThought

class FeedsThoughtTest(unittest.TestCase):

    def setUp(self):
        self.argv = ['think', 'feeds']

    @patch('feeds_thought.all')
    def test_list(self, all):
        all.return_value = [
            {'name': 'http://address.com/feed'}
        ]
        t = FeedsThought()
        self.argv.append('list')
        self.assertEquals("http://address.com/feed", t.list(self.argv))

    @patch('feeds_thought.save_in_table')
    @patch('feeds_thought.request')
    def test_add(self, request, save_in_table):
        self.argv.append('add')
        self.argv.append('http://address.com/feed')

        request.urlopen = self.__mock_request()
        t = FeedsThought()
        self.assertEquals("Address Feed", t.add(self.argv))

    @patch('feeds_thought.notify')
    @patch('feeds_thought.all')
    @patch('feeds_thought.request')
    def test_run(self, request, all, notify):
        all.return_value = [
            {'name': 'http://address.com/feed', 'value': []}
        ]
        request.urlopen = self.__mock_request()
        t = FeedsThought()
        t.run()
        notify.assert_called_with('Address Feed', 'Content Title')

    @patch('feeds_thought.notify')
    @patch('feeds_thought.all')
    @patch('feeds_thought.request')
    def test_run_not_notify_old_item(self, request, all, notify):
        all.return_value = [
            {'name': 'http://address.com/feed', 'value': ['Content Title']}
        ]
        request.urlopen = self.__mock_request()
        t = FeedsThought()
        t.run()
        self.assertFalse(notify.called)

    @patch('feeds_thought.notify')
    @patch('feeds_thought.all')
    @patch('feeds_thought.request')
    @patch('feeds_thought.save_in_table')
    def test_run_save_read_items(self, save_in_table, request, all, notify):
        all.return_value = [
            {'name': 'http://address.com/feed', 'value': []}
        ]
        request.urlopen = self.__mock_request()
        t = FeedsThought()
        t.run()
        value = save_in_table.call_args[0][2]
        self.assertTrue('Content Title' in value)

    def __mock_request(self):
        def urlopen(address):
            fixture = join(dirname(__file__), 'fixtures', 'atom.xml')
            return open(fixture)

        return urlopen

