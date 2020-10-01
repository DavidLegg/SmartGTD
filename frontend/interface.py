# Command-line user interface

from backend import *

def display_tasks():
    for task in LocalStore.tasks():
        print('[{}]  {}'.format('x' if task.completed else ' ', task.name))

def add_task():
    name = input('Name: ')
    task = Task(name, '')
    LocalStore.add_task(task)
