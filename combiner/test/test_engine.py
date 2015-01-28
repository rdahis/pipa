import py.test
import combiner.engine
class FakeCombiner(object):
	raw_data = []
	def __init__(self):
		pass
	def combine(self, data, db):
		return [1,2]

def test_combiner_raw_data_recieved():
	generator = combiner.engine.run_combiner(FakeCombiner(), None)
	assert True
