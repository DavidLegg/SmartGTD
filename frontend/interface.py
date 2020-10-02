# Command-line user interface

from util import *
from backend import *
import datetime as dt

WITH_YEAR_FMT = cfg('general', 'date_format', 'with_year')
NO_YEAR_FMT   = cfg('general', 'date_format', 'no_year')
RELATIVE_DAYS = cfg('general', 'relative_days')

def relative_date(d):
    '''Returns a description of date d, in # days before/after today if |d - today| is < relative_days.'''
    n = dt.date.today()
    if isinstance(d, dt.datetime):
        d = d.date()
    delta = (d - n).days
    if abs(delta) > RELATIVE_DAYS:
        return d.strftime(WITH_YEAR_FMT if abs(delta) > 150 else NO_YEAR_FMT)
    elif delta < -1:
        return '{} days ago'.format(abs(delta))
    elif delta == -1:
        return 'Yesterday'
    elif delta == 0:
        return 'Today'
    elif delta == 1:
        return 'Tomorrow'
    else:
        return 'In {} days'.format(delta)

def one_line(task, include_date = True):
    '''Constructs a one-line summary of task.'''
    date_str = relative_date(task.due_date) if include_date and task.due_date else ''

    return '[{}]  {:50} {:>20}'.format(
        'x' if task.completed else ' ',
        truncate(task.name, 50),
        date_str
        )

def display_tasks():
    for task in LocalStore.tasks():
        print(one_line(task))

def add_task():
    name = input('Add Task: ')
    task = Task(name, '')
    LocalStore.add_task(task)
