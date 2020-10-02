# Defines how to store and retrieve tasks

import json
from .config import cfg
from .types import *

class _LocalStore:
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

    def tasks(self):
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

LocalStore = _LocalStore()
