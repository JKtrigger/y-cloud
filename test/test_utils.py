import copy
import json

from src.telegram.utils import Event
from src.application import define_callbacks, listener
from test.unit.event import _from_menu


def test_active_callback_buttons():
    from_menu = copy.deepcopy(_from_menu)
    from_menu['callback_query']['data'] = "2023-may-1"
    # TODO to fixture
    from_menu = {'body': json.dumps(from_menu)}
    zzz = define_callbacks()
    # Todo divide test from lib test to application
    import ipdb
    ipdb.set_trace() # FIXME
    # listener.functions['calendar']['1'](from_menu, 1)
    listener.execute(Event(from_menu), 1)
    import ipdb
    ipdb.set_trace() # FIXME
