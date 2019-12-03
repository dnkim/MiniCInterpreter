from Function import FunctionEntry, FunctionTable
from Symbol import SymbolEntry, SymbolTable
from ParsedItems import ParsedFunc
from Result import *

SIZE = 0x4
BASE = 0x0000

class Frame:
	def __init__(self):
		self.function_table = FunctionTable()
		self.symbol_tables = [None, SymbolTable()]
		self.top = BASE
		self.flag = None

	# Handles frame to reflect scope for a new bracket
	def into_bracket(self):
		self.symbol_tables.append(SymbolTable())
		self.flag = True

	# Handles frame to reflect scope for a new function
	def into_function(self):
		self.symbol_tables.append(None)
		self.symbol_tables.append(SymbolTable())
		self.flag = False

	# Handles frame to reflect scope after escaping from bracket
	def escape_bracket(self):
		assert self.flag
		self.symbol_tables.pop()

	# Handles frame to reflect scope after escaping from function
	def escape_function(self):
		assert not self.flag
		self.symbol_tables.pop()
		self.symbol_tables.pop()

	# Private
	# Adds a new function
	def add_function(self, name, entry):
		return self.function_table.add(name, entry)

	# Private
	# Searches function for name
	def search_function(self, name):
		return self.function_table.search(name)

	# Declares corresponding function
	def declare_function(self, name, function):
		if self.add_function(name, FunctionEntry(function)):
			return Ok()
		else:
			return Err()

	# Returns corresponding functioin
	def get_function(self, name):
		entry = self.search_function(name)
		if entry:
			return Ok(entry.get_function())
		else:
			return Err()

	# Private
	# Adds a new symbol
	def add_symbol(self, name, entry):
		assert entry.address == self.top
		self.top += SIZE
		return self.symbol_tables[-1].add(name, entry)

	# Private
	# Searches symbol for name
	def search_symbol(self, name):
		for symbol_table in reversed(self.symbol_tables):
			if symbol_table:
				entry = symbol_table.search(name)
				if entry:
					return entry
			else:
				return None

	# Private
	# Returns address to be allocated
	def allocate_symbol(self):
		return self.top

	# Declares corresponding symbol
	def declare_symbol(self, name, line, is_int, length = None):
		if self.add_symbol(name, SymbolEntry(line, self.allocate_symbol(), is_int, length)):
			return Ok()
		else:
			return Err()

	# Returns corresponding type
	def get_type(self, name):
		entry = self.search_symbol(name)
		if entry:
			return Ok(entry.get_type())
		else:
			return Err()

	# Returns corresponding value
	# Should be called after validating type with get_type
	def get_value(self, name, index = None):
		entry = self.search_symbol(name)
		if entry:
			return Ok(entry.get_value(index))
		else:
			return Err()

	# Returns corresponding history
	# Should be called after validating type with get_type
	def get_history(self, name, index = None):
		entry = self.search_symbol(name)
		if entry:
			return Ok(entry.get_history(index))
		else:
			return Err()

	# Updates corresponding value
	# Should be called after validating type with get_type
	def update_value(self, name, line, value, index = None):
		entry = self.search_symbol(name)
		if entry:
			entry.update_value(line, value, index)
			return Ok()
		else:
			return Err()
