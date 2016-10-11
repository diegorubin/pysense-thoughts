from datetime import datetime

from sense.actions import notify
from sense.thought import ThoughtBase
from sense.memories import db, find_in_table, save_in_table

class TasksThought(ThoughtBase):
    def run(self):
        pass

    def lists(self, argv):
        lists = []
        for list in self.__table().all():
            lists.append(list['name'])
        return "\n".join(lists)

    def list(self, argv):
        list_name = argv[3]
        if self.__list_exists(list_name):
            tasks = self.__get_tasks(list_name)
            return "\n".join(tasks)
        else:
            return 'not found'

    def insert(self, argv):
        list_name = argv[3]

        tasks = self.__get_tasks(list_name)

        tasks.append(argv[4])
        save_in_table(self.__table(), list_name, tasks)
        return "\n".join(tasks)

    def remove(self, argv):
        list_name = argv[3]
        item = int(argv[4])

        tasks = self.__get_tasks(list_name)

        del tasks[item]

        save_in_table(self.__table(), list_name, tasks)
        return "\n".join(tasks)


    def __list_exists(self, list_name):
        list_entry = find_in_table(self.__table(), list_name)

        return len(list_entry) != 0

    def __table(self):
        return db().table('tasks')

    def __get_tasks(self, list_name):
        tasks = find_in_table(self.__table(), list_name)

        if len(tasks) == 0:
            tasks = []
        else:
            tasks = tasks[0]['value']

        return tasks


def init():
    thought = TasksThought()
    return thought

