class _Singleton:
	__shared_state = {}
	def __init__(self):
		self.__dict__ = self.__shared_state

	RAW_DATA_DIR = 'tmp/raw'

settings = _Singleton()
