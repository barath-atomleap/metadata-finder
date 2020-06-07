# flake8: noqa F401
from .bing import __bing_find
from .wikipedia import __wikipedia_find
from .clearbit import __clearbit_find

finders = {'bing': __bing_find, 'wikipedia': __wikipedia_find, 'clearbit': __clearbit_find}
