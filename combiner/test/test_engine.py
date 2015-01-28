import py.test
import combiner.engine
from combiner.settings import settings
import os

raw_filename = 'combiner_test_engine'

class TestEngine():
	def setup_class(self):
		import copy
		self.old_settings = copy.copy(settings.__dict__)
		settings.RAW_DATA_DIR = "/tmp"

	def teardown_class(self):
		settings.__dict__ = self.old_settings

	def test_combiner_raw_data_recieved(self):
		class FakeCombiner(object):
			raw_data = [raw_filename]
			def __init__(self):
				with open('/tmp/' + raw_filename + '.csv', 'w') as f:
					f.write("f1,f2\na,b\nc,d")
			def combine(self, data, db):
				assert data.combiner_test_engine
				assert len(data) == 1
				assert list(data.combiner_test_engine) == [{'f1':'a', 'f2':'b'},{'f1':'c', 'f2':'d'}]
				return []
		generator = combiner.engine.run_combiner(FakeCombiner(), None)
		list(generator) # consume generator to turn engine on!
