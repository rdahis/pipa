#!/usr/bin/env python2.7
import unittest
from combiner.util import transform_dict

class TestCombinerUtil(unittest.TestCase):
	def test_transform_dict_simple(self):
		start = {'name': 'fred', 'age':4}
		translate = {'name': 'nome', 'age':'idade'}
		expected = {'nome': 'fred', 'idade':4}
		self.assertEqual(transform_dict(start, translate), expected)

	def test_transform_dict_kill_keys(self):
		start = {'killme':5}
		translate = {'killme': None}
		expected = {}
		self.assertEqual(transform_dict(start, translate), expected)


if __name__ == '__main__':
	unittest.main()
