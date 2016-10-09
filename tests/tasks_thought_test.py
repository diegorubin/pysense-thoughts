import unittest
from unittest.mock import patch

from tasks_thought import TasksThought

class TasksThoughtTest(unittest.TestCase):

    def setUp(self):
        self.argv = ['think', 'task']

    @patch('tasks_thought.save_in_table')
    def test_insert(self, save_in_table):
        self.argv.append('insert')
        self.argv.append('list name')
        self.argv.append('description')

        t = TasksThought()
        self.assertEquals('description', t.insert(self.argv))

    def test_list_not_found(self):
        self.argv.append('list')
        self.argv.append('not exists')

        t = TasksThought()
        self.assertEquals('not found', t.list(self.argv))

    @patch('tasks_thought.find_in_table')
    def test_list_found(self, find_in_table):
        find_in_table.return_value = [{'name': 'list name', 'value': ['an entry']}]
        self.argv.append('list')
        self.argv.append('exists')

        t = TasksThought()
        self.assertEquals('an entry', t.list(self.argv))

