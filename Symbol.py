VAR_SIZE = 0x4

class SymbolEntry:
	def __init__(self, line, address, is_int, length = None):
		self.is_int = is_int
		self.length = length
		self.address = address
		self.values = []
		if self.length is not None:
			for i in range(self.length):
				self.values += [[(line, None)]]
			self.values += [[(line, self.address)]]
		else:
			self.values += [(line, None)]

	# Returns corresponding type
	def get_type(self):
		return (self.is_int, self.length)

	# Returns corresponding value
	def get_value(self, index = None):
		return self.get_history(index)[-1][1]

	# Returns corresponding history
	def get_history(self, index = None):
		if index is None:
			if self.length is None:
				return self.values
			else:
				return self.values[-1]
		else:
			assert self.length is not None
			assert 0 <= index < self.length
			return self.values[index]

	# Updates corresponding value
	def update_value(self, line, value, index = None):
		if index is None:
			assert self.length is None
			self.values.append((line, value))
		else:
			assert self.length is not None
			assert 0 <= index < self.length
			self.values[index].append((line, value))

class SymbolTable:
	def __init__(self, top = 0x0000):
		self.symbols = {}
		self.top = top

	# Adds a new symbol
	def add(self, name, entry):
		assert entry.address == self.top
		if name in self.symbols:
			return False
		self.symbols[name] = entry
		self.top += VAR_SIZE
		return True

	# Searches symbol for name
	def search(self, name):
		try:
			return self.symbols[name]
		except KeyError:
			return None

	# Returns address to be allocated
	def allocate(self):
		return self.top

	# Used when entering into a new bracket or function
	def above(self):
		return SymbolTable(self.top)
