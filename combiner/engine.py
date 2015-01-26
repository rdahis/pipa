#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

from argcomplete import autocomplete
from argparse import ArgumentParser
from unicodecsv import DictReader
from combiner import valid_combiners
import combiner
import io
from collections import namedtuple
from combiner.util import db_connect

RAW_DATA_DIR = 'tmp/raw'

def main():
	parser = ArgumentParser(description='Run a combiner')
	parser.add_argument('combiner', type=str, help='the combiner name to be run', 
			choices=valid_combiners)
	autocomplete(parser, always_complete_options=False)
	args = parser.parse_args()

	try:
		chosen_combiner = __import__(args.combiner, combiner)
	except ImportError:
		print("combiner '%s' does not exist" % args.combiner)
		raise
	requested_data = chosen_combiner.raw_data

	session = db_connect(chosen_combiner)
	Data = namedtuple(args.combiner + '_data', requested_data)
	files = []
	try:
		# Accumulator pattern is needed in this case
		for f in requested_data:
			f = RAW_DATA_DIR + '/' + f + '.csv'
			files.append(io.open(f, 'rb'))
			data = map(lambda x: DictReader(x, encoding='utf8'), files)
			data = Data(*data)
		for item in chosen_combiner.combine(data):
			_send_to_db(session, item)
	finally:
		for f in files: f.__exit__()

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
