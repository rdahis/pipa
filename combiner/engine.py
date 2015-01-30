#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

from argcomplete import autocomplete
from argparse import ArgumentParser
from unicodecsv import DictReader
from combiner import valid_combiners
import io
from collections import namedtuple
from combiner.util import db_connect

from combiner.settings import settings
from glob import glob
import json
import os

# TODO: logs
# TODO: Turn into proper python package

SUPPORTED_FORMATS = ('csv', 'jsonlines')

def main():
	args = _get_user_input()
	combiner_module = _load_a_combiner(args.combiner)
	session = db_connect()
	iter_results = run_combiner(combiner_module, session)
	_store_on_db(iter_results, session)

def run_combiner(combiner_module, db_session):
	with _load_raw_data(combiner_module.raw_data) as data:
		for item in combiner_module.combine(data, db_session): yield item
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
			data = []
			# Accumulator pattern is needed in this case
			for f in raw_data_list:
				file, reader = _get_file_and_reader_from_basename(f)
				self.files.append(file)
				data.append(reader)
			return RawData(*data)
		def __exit__(self, *exception):
			for f in self.files: f.__exit__()
	return ctx_manager()

def _get_file_and_reader_from_basename(path):
	path = settings.RAW_DATA_DIR + '/' + path
	filenames = glob(path + '.*')
	filenames = list(filter(lambda fn: fn[len(path)+1:] in SUPPORTED_FORMATS, filenames))
	if len(filenames) > 1: raise Exception('Ambiguous raw_file name: "%s"! There are more than one possible raw files: %s' % (path, filenames))
	if not filenames: raise Exception('No rawfiles found for "%s"' % path)
	filename = filenames[0]
	extension = filename[len(path)+1:]
	file = open(filename, 'r')
	if extension == 'csv':
		reader = DictReader(file, encoding='utf8')
	elif extension == 'jsonlines':
		def JsonLinesReader(f):
			for line in f:
				yield json.loads(line)
		reader = JsonLinesReader(file)
	return file, reader

def _load_a_combiner(combiner_name):
	from importlib import import_module
	import combiner
	try:
		return import_module('combiner.' + combiner_name)
	except ImportError:
		print("Error! Combiner '%s' does not exist" % combiner_name)
		raise

def _store_on_db(iter_results, session):
	#TODO: meter um with aqui pra fechar a conexao
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
