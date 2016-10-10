import unittest
from unittest.mock import patch

from tasks_thought import TasksThought

class TasksThoughtTest(unittest.TestCase):

    def setUp(self):
        self.argv = ['think', 'task']

    @patch('tasks_thought.db')
    def test_lists(self, table):
        class TableMocked:
            def all(self):
                return [
                    {'name': 'lista 1'},
                    {'name': 'lista 2'}
                ]

        class DbMocked:
            def table(self, table):
                return TableMocked()
        table.return_value = DbMocked()

        self.argv.append('lists')

        t = TasksThought()
        self.assertEquals("lista 1\nlista 2", t.lists(self.argv))

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

    @patch('tasks_thought.find_in_table')
    @patch('tasks_thought.save_in_table')
    def test_insert(self, find_in_table, save_in_table):
        find_in_table.return_value = [
            {'name': 'list name', 'value': ['one', 'two', 'three']}
        ]

        self.argv.append('remove')
        self.argv.append('list name')
        self.argv.append('1')

        t = TasksThought()
        self.assertEquals("one\nthree", t.remove(self.argv))

