# Command-line user interface

from util import *
from backend import *
import datetime as dt
import curses

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

def display_tasks():
    for task in LocalStore.tasks():
        print(one_line(task))

def gtd_display():
    for tag in DEFAULT_TAGS:
        print(HEADER(tag))
        for task in LocalStore.with_tags([tag]):
            print(one_line(task))

def add_task():
    name = input('Add Task: ')
    task = Task(name, '')
    LocalStore.add_task(task)

def select_task():
    selected_task = None

    def select_task_main(stdscr):
        nonlocal selected_task
        curses.curs_set(False)
        active_line   = 0
        max_lines     = curses.LINES - 1
        query         = ''
        query_changed = False
        all_tasks     = LocalStore.tasks()
        tasks         = all_tasks[:max_lines]
        c = 0

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, '> ')
            if query_changed:
                if query == '':
                    tasks = all_tasks[:max_lines]
                else:
                    tasks = fuzzy_search(query, all_tasks)[:max_lines]
            active_line = min(active_line, len(tasks))
            stdscr.addstr(0, 2, query)
            for i, t in enumerate(tasks, 1):
                if i == active_line:
                    stdscr.addstr(i, 0, one_line(t), curses.A_REVERSE)
                else:
                    stdscr.addstr(i, 0, one_line(t))

            c = stdscr.getch()
            if c == curses.KEY_UP and active_line > 0:
                active_line -= 1
            elif c == curses.KEY_DOWN and active_line < len(tasks):
                active_line += 1
            elif c == curses.KEY_BACKSPACE:
                query = query[:-1]
                query_changed = True
            elif c == ord('\n') and active_line > 0:
                selected_task = tasks[active_line - 1]
                break
            elif chr(c).isprintable():
                query += chr(c)
                query_changed = True


    curses.wrapper(select_task_main)

    return selected_task
