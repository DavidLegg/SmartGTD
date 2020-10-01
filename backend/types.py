# Contains definitions for data types

from uuid import uuid4

class Task:
    def __init__(self, name, notes, id = None, completed = False):
        self.name       = name
        self.notes      = notes
        self.id         = str(uuid4()) if id is None else id
        self.completed  = completed

    def to_json(self):
        return {
            'name': self.name,
            'notes': self.notes,
            'id': self.id,
            'completed': self.completed
        }

    @staticmethod
    def from_json(obj):
        return Task(obj['name'], obj['notes'], id = obj['id'], completed = obj['completed'])

    def __str__(self):
        return '{} ({})'.format(name, id)

    def __repr__(self):
        return 'Task({r}, {r}, id = {r}, completed = {r})'.format(name, notes, id, completed)
