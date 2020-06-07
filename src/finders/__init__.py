# flake8: noqa F401
from .bing import __bing_find
from .wikipedia import __wikipedia_find
from .clearbit import __clearbit_find
from .google_graph import __google_graph_find
from .diffbot import __diffbot_find
from utils.decorators import async_wrap
finders = {
    'bing': async_wrap(__bing_find),
    'wikipedia': async_wrap(__wikipedia_find),
    'clearbit': async_wrap(__clearbit_find),
    'google-graph': async_wrap(__google_graph_find),
    'diffbot': async_wrap(__diffbot_find)
}
