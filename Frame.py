from Function import FunctionEntry, FunctionTable
from Symbol import SymbolEntry, SymbolTable
from ParsedItems import ParsedFunc

class Frame:
	def __init__(self):
		self._function_table = FunctionTable()
		self._symbol_tables = [SymbolTable()]

	# Handles frame to reflect scope for a new bracket
	def into_bracket(self):
		#unimplemented

	# Handles frame to reflect scope for a new function
	def into_function(self):
		#unimplemented

	# Handles frame to reflect scope after escaping from bracket or function
	def escape_scope(self):
		#unimplemented

	# Adds a new function
	def add_function(self, name, function):
		#unimplemented

	# Returns corresponding function
	def get_function(self, name):
		#unimplemented

	# Adds a new symbol
	def add_symbol(self, name, is_int, length = None):
		#unimplemented

	# Returns corresponding value
	def get_value(self, name, index = None):
		#unimplemented

	# Returns corresponding history
	def get_history(self, name):
		#unimplemented

	# Updates corresponding value
	def update_value(self, name, is_int, value, index = None):
		#unimplemented
