from murko.config import Config
import pytest


class TestConfig:

	def test_getter_and_setter(self):
		c = Config()
		c['x'] = 1 
		c['nested:x'] = 2
		c['nested:even:more:x'] = 3

		assert c['x'] == 1
		assert c['nested:x'] == 2
		assert c['nested']['x'] == 2
		assert c['nested:even:more:x'] == 3
		assert c['nested']['even']['more']['x'] == 3

	def test_leaves(self):
		c = Config()
		c['x'] = 1 
		c['nested:x'] = 2
		c['nested:y'] = 3	
		c['nested:some:more:y'] = 4

		c.set_label(attach=[], abbr={'nested:some:more:y':'yay'})

		expected = [('x',1), ('x',2), ('y',3), ('yay',4)]
		actual   = c.leaves
		assert all([a == b for a, b in zip(actual, expected)])


	def test_label(self):
		c = Config()
		c['x'] = 1
		c['nested:x'] = 2
		c['nested:y'] = 3

		c.set_label(attach = ["x", "nested:x"], 
					abbr   = {"nested:x": "xx"})	

		assert c.label == "x1_xx2"

	def test_bunch(self):
		c = Config()
		c['x'] = 1
		c['nested:x'] = 2
		c['nested:y'] = 3
		b = c.bunch
		assert b.nested.x == 2

