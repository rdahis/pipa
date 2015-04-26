from functools import wraps
import shelve
import inspect

class DownloadController(object):
	class SKIPPED: pass
	def __init__(self, filename, logger):
		self.stack = []
		self.shelve = shelve.open(filename, 'c', writeback=True)
		self.shelve.setdefault('download_control', {})
		self.logger = logger

	def apply_control(self, fun):
		control_key_param_present = 'control_key' in inspect.getargspec(fun).args
		@wraps(fun)
		def decorated(*a, **kw):
			control_key = kw['control_key']
			if not control_key_param_present: del kw['control_key']
			self.stack.append(control_key)
			try:
				if self.check_if_completed():
					return self.SKIPPED
				ret = fun(*a, **kw)
				if ret: self.success()
				else: self.failure(ret)
				return ret
			except Exception as e:
				self.failure(e)
				raise
			finally: self.stack.pop()
		return decorated
	
	def check_if_completed(self):
		d = self.shelve['download_control']
		for key in self.stack:
			d = d.get(key, {})
		if d.get('complete') == True:
			self.logger.info('skipping, already completed: ' + key)
			return True
		return False

	def failure(self, e):
		self.logger.error('failure during %s' % self.stack)
		self.logger.error('exception:  %s' % e)

	def success(self):
		d = self.shelve['download_control']
		for key in self.stack:
			d.setdefault(key, {})
			d = d[key]
		d['complete'] = True
		self.shelve.sync()

	def __del__(self):
		self.shelve.close()

if __name__ == '__main__':
	import shelve
	control = shelve.open('tmp/ffdownloads/control.dbm', 'r')
	from pprint import pprint
	import json
	print json.dumps(control['download_control'], indent=4, sort_keys=True)
