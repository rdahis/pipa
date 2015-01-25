"""
A combiner is 1-1 to a database table, it should know how to combine raw
data to insert entries into the table.
"""
import os
valid_combiners = os.listdir(os.path.dirname(os.path.realpath(__file__)))
valid_combiners = [v[:-3] for v in valid_combiners if v not in ('__init__.py', 'engine.py', 'util.py') and v[-3:] == '.py']
__all__ = valid_combiners
