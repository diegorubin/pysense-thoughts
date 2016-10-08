from datetime import datetime
from subprocess import call
from os import chdir

from sense.actions import notify
from sense.thought import ThoughtBase
from sense.memories import db

class TasksThought(ThoughtBase):
    def run(self):
	pass

    def list(self, argv):
        list_name = argv[3]
        return 'ok'

    def insert(self, argv):
        list_name = argv[3]
        if self.__list_exists(list_name):
            return true
        return false

    def __list_exists(self, list_name):
        query = Query()
        list_entry = self.__table().search(query.name == list_name)

        return len(list_entry) != 0

    def __table(self):
        return db().table('tasks')

def init():
    thought = TasksThought()
    return thought

