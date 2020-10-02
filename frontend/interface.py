# Command-line user interface

from util import *
from backend import *
from .console_utils import *
import datetime as dt
import curses, string

WITH_YEAR_FMT = cfg('general', 'date_format', 'with_year')
NO_YEAR_FMT   = cfg('general', 'date_format', 'no_year')
RELATIVE_DAYS = cfg('general', 'relative_days')
DEFAULT_TAGS  = cfg('general', 'default_tags')
HEADER        = cfg('general', 'header_format').format

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

def search_content(task):
    return ' '.join((
        task.name,
        task.notes,
        ' '.join(task.tags),
        relative_date(task.due_date) if task.due_date else ''))

def display_tasks():
    for task in Tasks.all():
        print(one_line(task))

def _tag_display(tags):
    for tag in tags:
        print(HEADER(tag))
        for task in Tasks.with_tags([tag]):
            print(one_line(task))

def gtd_display():
    _tag_display(DEFAULT_TAGS)

def tag_display():
    tags = input('Tags: ').split()
    _tag_display(tags)

def add_task():
    name = input('Add Task: ')
    task = Task(name, '')
    Tasks.add_task(task)

def select_task():
    lines = [SelectLine(one_line(t), search_content(t), t) for t in Tasks.all()]
    return interactive_select(lines)

def complete_task():
    task = select_task()
    task.completed = True
    Tasks.save()

def add_tag():
    task = select_task()
    tag  = input('Tag: ')
    task.tags.add(tag)
    Tasks.save()

def change_due_date():
    task = select_task()
    s = input('Due date: ')
    while s != '' and default(lambda: date_parse(s)) is None:
        print('Invalid date format. Use empty input to remove due date.')
    task.due_date = default(lambda: date_parse(s))
    Tasks.save()

def focus_tasks():
    explicit  = Tasks.with_tags(['focus'])
    overdue   = Tasks.due_before(dt.date.today())
    due_today = Tasks.due_on(dt.date.today())
    overdue   = [t for t in overdue if t not in explicit]
    due_today = [t for t in due_today if t not in explicit and t not in overdue]
