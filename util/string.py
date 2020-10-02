# Collection of string utility functions

def truncate(s, max_len):
    '''If s is longer than max_len, truncates and adds an ellipsis.'''
    if len(s) < max_len:
        return s
    elif max_len > 3:
        return s[:max_len - 3] + '...'
    else:
        return '.' * max_len
