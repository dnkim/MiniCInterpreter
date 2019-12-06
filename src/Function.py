from ParsedItems import ParsedFunc

class FunctionEntry:
	def __init__(self, function):
		self.function = function

	# Returns corresponding function
	def get_function(self):
		return self.function

class FunctionTable:
	def __init__(self):
		self.functions = {}

	# Adds a new function
	def add(self, name, entry):
		if name in self.functions:
			return False
		self.functions[name] = entry
		return True

	# Searches function for name
	def search(self, name):
		try:
			return self.functions[name]
		except KeyError:
			return None
