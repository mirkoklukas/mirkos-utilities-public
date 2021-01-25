from murko.config import ConfigSpace

import pytest



class TestConfigSpace:
	def test_getter_and_setter(self):

		cs = ConfigSpace(order="col")
		cs.add("x", [1,2,3])
		cs.add("test:y", [11,12,13])
		cs.add("test:z", 'lambda: test.y - x')


		assert cs[0]["x"] == 1
		assert cs[0]["test:y"] == 11
		assert cs[0]["test:z"] == 10
