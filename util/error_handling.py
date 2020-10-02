# Collection of defualt error handling behavior, wrapping lambda calls with try-except blocks

def default(action, default_value = None):
    '''Returns a default_value if action fails.'''
    try:
        return action()
    except:
        return default_value
