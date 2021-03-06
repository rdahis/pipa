import py.test
import combiner.engine
from combiner.settings import settings
import os

class TestEngine():
	def setup_method(self, method):
		self.method_name = method.__name__

	def setup_class(self):
		import copy
		self.old_settings = copy.copy(settings.__dict__)
		settings.RAW_DATA_DIR = "/tmp"

	def teardown_class(self):
		settings.__dict__ = self.old_settings

	def test_combiner_raw_data_csv_recieved(self):
		raw_filename = self.method_name
		class FakeCombiner(object):
			raw_data = [raw_filename]
			def __init__(self):
				with open('/tmp/' + raw_filename + '.csv', 'w') as f:
					f.write("f1,f2\na,b\nc,d")
			def combine(self, data, db):
				assert hasattr(data, raw_filename)
				assert len(data) == 1
				assert list(data[0]) == [{'f1':'a', 'f2':'b'},{'f1':'c', 'f2':'d'}]
				return []
		generator = combiner.engine.run_combiner(FakeCombiner(), None)
		list(generator) # consume generator to turn engine on!

	def test_combiner_raw_data_jsonlines_recieved(self):
		raw_filename = self.method_name
		class FakeCombiner(object):
			raw_data = [raw_filename]
			def __init__(self):
				with open('/tmp/' + raw_filename + '.jsonlines', 'w') as f:
					f.write('{"f1":{"ff1":1, "ff2":2}}\n{"f1":1}')
			def combine(self, data, db):
				assert len(data) == 1
				assert list(data[0]) == [{'f1':{'ff1':1, 'ff2':2}}, {'f1':1}]
				return []
		generator = combiner.engine.run_combiner(FakeCombiner(), None)
		list(generator) # consume generator to turn engine on!
