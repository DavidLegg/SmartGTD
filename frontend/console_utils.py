# Utilities for building a command-line interface

import curses, string
from collections import namedtuple

SelectLine = namedtuple('SelectLine', ['display', 'search', 'value'])

def fuzzy_search(query, lines):
    terms = query.split()
    return [line for line in lines if all(term in line.search for term in terms)]

def interactive_select(lines, case_sensitive=False):
    '''Takes a list of SelectLines, implements an interactive fuzzy-search selection algorithm.'''
    selected_value = None
    if not case_sensitive:
        lines = [SelectLine(line.display, line.search.lower(), line.value) for line in lines]

    def select_main(stdscr):
        nonlocal selected_value
        curses.curs_set(False)
        cursor_line   = 1
        max_lines     = curses.LINES - 1
        query         = ''
        query_changed = False
        active_lines  = lines[:max_lines]
        c = 0

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, '> ')
            if query_changed:
                if query == '':
                    active_lines = lines[:max_lines]
                else:
                    if not case_sensitive:
                        query = query.lower()
                    active_lines = fuzzy_search(query, lines)[:max_lines]
            cursor_line = max(1, min(cursor_line, len(active_lines)))
            stdscr.addstr(0, 2, query)
            if active_lines:
                for i, line in enumerate(active_lines, 1):
                    if i == cursor_line:
                        stdscr.addstr(i, 0, line.display, curses.A_REVERSE)
                    else:
                        stdscr.addstr(i, 0, line.display)
            else:
                stdscr.addstr(1, 0, '- No results -')

            try:
                c = stdscr.getch()
            except KeyboardInterrupt:
                stdscr.getch() # work-around, catches a stray byte in the input stream
                break
            if c == curses.KEY_UP and cursor_line > 1:
                cursor_line -= 1
            elif c == curses.KEY_DOWN and cursor_line < len(active_lines):
                cursor_line += 1
            elif c == curses.KEY_BACKSPACE:
                query = query[:-1]
                query_changed = True
            elif c == 27: # ESC
                break
            elif c == ord('\n') and active_lines:
                selected_value = active_lines[cursor_line - 1].value
                break
            elif chr(c) in string.printable:
                query += chr(c)
                query_changed = True


    curses.wrapper(select_main)

    return selected_value
