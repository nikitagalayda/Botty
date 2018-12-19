from transitions.extensions import Machine
#import pygraphviz

from joke_fact_generator import *

states = ['init', 'joke', 'fun_fact', 'request', 'parks', 'museums', 'historic_sites', 'satisfy_check']
transitions = [
	{'trigger': 'make_joke', 'source': 'init', 'dest': 'joke'},
	{'trigger': 'request', 'source': 'init', 'dest': 'request'},
	{'trigger': 'give_fact', 'source': 'init', 'dest': 'fun_fact'},

	{'trigger': 'make_joke', 'source': 'fun_fact', 'dest': 'joke'},
	{'trigger': 'request', 'source': 'fun_fact', 'dest': 'request'},
	{'trigger': 'goto_init', 'source': 'fun_fact', 'dest': 'init'},
	{'trigger': 'give_fact', 'source': 'fun_fact', 'dest': 'fun_fact'},

	{'trigger': 'request', 'source': 'joke', 'dest': 'request'},
	{'trigger': 'goto_init', 'source': 'joke', 'dest': 'init'},
	{'trigger': 'give_fact', 'source': 'joke', 'dest': 'fun_fact'},
	{'trigger': 'make_joke', 'source': 'joke', 'dest': 'joke'},
	
	{'trigger': 'park_choice', 'source': 'request', 'dest': 'parks'},
	{'trigger': 'museum_choice', 'source': 'request', 'dest': 'museums'},
	{'trigger': 'history_choice', 'source': 'request', 'dest': 'historic_sites'},
	{'trigger': 'goto_init', 'source': 'request', 'dest': 'init'},

	{'trigger': 'satisfy_check', 'source': 'parks', 'dest': 'satisfy_check'},
	{'trigger': 'goto_init', 'source': 'parks', 'dest': 'init'},

	{'trigger': 'satisfy_check', 'source': 'museums', 'dest': 'satisfy_check'},
	{'trigger': 'goto_init', 'source': 'museums', 'dest': 'init'},

	{'trigger': 'satisfy_check', 'source': 'historic_sites', 'dest': 'satisfy_check'},
	{'trigger': 'goto_init', 'source': 'historic_sites', 'dest': 'init'},

	{'trigger': 'not_satisfied', 'source': 'satisfy_check', 'dest': 'request'},
	{'trigger': 'satisfied', 'source': 'satisfy_check', 'dest': 'init'},
	{'trigger': 'goto_init', 'source': 'satisfy_check', 'dest': 'init'}
	]

class StateMachine():
	def __init__(self, **machine_settings):
		self.machine = Machine(model = self, **machine_settings)
		