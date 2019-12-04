class SymbolEntry:
	def __init__(self, line, is_int, is_pointer = None, value = None):
		self.is_int = is_int
		self.is_pointer = is_pointer
		self.values = []
		self.values += [(line, value)]

	# Returns corresponding type
	def get_type(self):
		return (self.is_int, self.is_pointer)

	# Returns corresponding value
	def get_value(self):
		return self.is_int, self.is_pointer, self.values[-1][1]

	# Returns corresponding history
	def get_history(self):
		return self.values

	# Updates corresponding value
	def update_value(self, line, value):
		self.values.append((line, value))

class SymbolTable:
	def __init__(self):
		self.symbols = {}

	# Adds a new symbol
	def add(self, name, entry):
		if name in self.symbols:
			return False
		self.symbols[name] = entry
		return True

	# Searches symbol for name
	def search(self, name):
		try:
			return self.symbols[name]
		except KeyError:
			return None
