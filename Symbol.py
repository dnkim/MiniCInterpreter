class SymbolEntry:
	def __init__(self, address, is_int, length = None):
		self._address = address
		self._is_int = is_int
		self._length = length
		self._values = []

	# Returns corresponding value
	def get_value(self, index = None):
		#unimplemented

	# Returns corresponding history
	def get_history(self):
		return self._values

	# Updates corresponding value
	def update_value(self, is_int, value, index = None):
		#unimplemented

class SymbolTable:
	def __init__(self, top = 0x0000):
		self._symbols = {}
		self._top = top

	# Adds a new symbol
	def add(self, name, entry):
		#unimplemented

	# Searches symbol for name
	def search(self, name):
		#unimplemented

	# Used when entering into a new bracket or function
	# Copies values if flag is True
	def copy(self, flag = True):
		#unimplemented
