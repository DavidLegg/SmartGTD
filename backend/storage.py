# Defines how to store and retrieve tasks

import json
from .config import cfg
from .types import *

class LocalStore:
    def __init__(self):
        self._filename = cfg('general', 'local_store')
        try:
            with open(self._filename) as f:
                data = json.load(f)
                self._tasks = {x.id:x for x in (Task.from_json(t) for t in data['tasks'])}
                self._misc  = data['misc']
        except FileNotFoundError:
            self._tasks = {}
            self._misc  = {}

    def add_task(self, task):
        self._tasks[task.id] = task
        self.save()

    def all(self):
        return list(self._tasks.values())

    def add_misc(self, key, value):
        self._misc[key] = value

    def save(self):
        data = {'tasks': [t.to_json() for t in self._tasks.values()], 'misc': self._misc}
        with open(self._filename, 'w') as f:
            json.dump(data, f)

    def with_tags(self, tags):
        '''Returns a list of tasks with all specified tags.'''
        return [t for t in self._tasks.values() if all(tag in t.tags for tag in tags)]

    def due_before(self, date):
        '''Returns a list of tasks due (strictly) before the given date.'''
        return [t for t in self._tasks.values() if t.due_date is not None and t.due_date < date]

    def due_on(self, date):
        '''Returns a list of tasks due on the given date. Pass None to date to find tasks with no due date.'''
        return [t for t in self._tasks.values() if t.due_date is not None and t.due_date == date]


Tasks = LocalStore()
