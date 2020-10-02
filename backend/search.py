# Functions to search through a list of tasks

from .config import *

_FUZZY_NAME_WT = cfg('general', 'fuzzy_search', 'weights', 'name')
_FUZZY_NOTES_WT = cfg('general', 'fuzzy_search', 'weights', 'notes')
_FUZZY_TAG_EXACT_WT = cfg('general', 'fuzzy_search', 'weights', 'tag_exact')
_FUZZY_TAG_PARTIAL_WT = cfg('general', 'fuzzy_search', 'weights', 'tag_partial')

# TODO: this needs serious re-working. The behavior is very non-intuitive.
def fuzzy_search(query, tasks):
    terms = query.split()
    def match_score(task):
        return sum((
                (term in task.name)  * _FUZZY_NAME_WT +
                (term in task.notes) * _FUZZY_NOTES_WT +
                (term in task.tags)  * _FUZZY_TAG_EXACT_WT +
                any(term in tag for tag in task.tags) * _FUZZY_TAG_PARTIAL_WT
            ) for term in terms)

    tasks = [(match_score(t), t) for t in tasks]
    tasks = sorted((x for x in tasks if x[0] > 0), key = lambda x: x[0])
    return [t for _,t in tasks]
