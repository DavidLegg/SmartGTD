# Contains definitions for data types

from util import *
from uuid import uuid4
import datetime as dt
from dateutil.parser import isoparse

class Task:
    def __init__(self, name, notes = '', due_date = None, id = None, completed = False, tags = None):
        self.name       = name
        self.notes      = notes
        self.due_date   = due_date
        self.id         = str(uuid4()) if id is None else id
        self.completed  = completed
        self.tags       = set() if tags is None else set(tags)

    def tag(self, t):
        self.tags.add(t)

    def to_json(self):
        return {
            'name'     : self.name,
            'notes'    : self.notes,
            'id'       : self.id,
            'completed': self.completed,
            'due_date' : default(lambda: self.due_date.isoformat()),
            'tags'     : [str(t) for t in tags]
        }

    @staticmethod
    def from_json(obj):
        return Task(obj['name'], obj['notes'],
                id        = obj['id'],
                completed = obj.get('completed', False),
                due_date  = default(lambda: isoparse(obj['due_date'])),
                tags      = obj.get('tags', None)
            )

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)

    def __repr__(self):
        return 'Task({!r}, {!r}, id = {!r}, completed = {!r}, due_date = {!r})'.format(self.name, self.notes, self.id, self.completed, self.due_date)
