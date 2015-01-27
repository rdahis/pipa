#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

from argcomplete import autocomplete
from argparse import ArgumentParser
from unicodecsv import DictReader
from combiner import valid_combiners
import io
from collections import namedtuple
from combiner.util import db_connect

RAW_DATA_DIR = 'tmp/raw'

def main():
	args = _get_user_input()
	combiner_module = _load_a_combiner(args.combiner)
	iter_results = run_combiner(combiner_module)
	_store_on_db(iter_results)

def run_combiner(combiner_module):
	with _load_raw_data(combiner_module.raw_data) as data:
		for item in combiner_module.combine(data): yield item
		# This generator is needed so that with does not close files

def _get_user_input():
	parser = ArgumentParser(description='Run a combiner')
	parser.add_argument('combiner', type=str, help='the combiner name to be run', 
			choices=valid_combiners)
	autocomplete(parser, always_complete_options=False)
	return parser.parse_args()

def _load_raw_data(raw_data_list):
	RawData = namedtuple('RawData', raw_data_list)
	class ctx_manager(object):
		def __enter__(self):
			self.files = []
			# Accumulator pattern is needed in this case
			for f in raw_data_list:
				f = RAW_DATA_DIR + '/' + f + '.csv'
				self.files.append(io.open(f, 'rb'))
			data = map(lambda x: DictReader(x, encoding='utf8'), self.files)
			return RawData(*data)
		def __exit__(self, *exception):
			for f in self.files: f.__exit__()
	return ctx_manager()

def _load_a_combiner(combiner_name):
	from importlib import import_module
	import combiner
	try:
		return import_module('combiner.' + combiner_name)
	except ImportError:
		print("Error! Combiner '%s' does not exist" % combiner_name)
		raise

def _store_on_db(iter_results):
	#TODO: meter um with aqui pra fechar a conexao
	session = db_connect()
	for item in iter_results:
		_send_to_db(session, item)

def _send_to_db(session, item):
	try:
		session.add(item)
		session.commit()
		session.flush()
	except:
		session.rollback()
		raise

if __name__ == '__main__':
	main()
