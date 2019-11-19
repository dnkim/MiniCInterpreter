from ParsedItems import ParsedFunc

class FunctionEntry:
	def __init__(self, function):
		self._function = function

	# Returns corresponding function
	def get_function(self):
		return self._function

class FunctionTable:
	def __init__(self):
		self._functions = {}

	# Adds a new function
	def add(self, name, entry):
		#unimplemented

	# Searches function for name
	def search(self, name):
		#unimplemented
