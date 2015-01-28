#!/usr/bin/env python2.7
from combiner.util import transform_dict

def test_transform_dict_simple():
	start = {'name': 'fred', 'age':4}
	translate = {'name': 'nome', 'age':'idade'}
	expected = {'nome': 'fred', 'idade':4}
	assert transform_dict(start, translate) == expected

def test_transform_dict_kill_keys():
	start = {'killme':5}
	translate = {'killme': None}
	expected = {}
	assert transform_dict(start, translate) == expected
