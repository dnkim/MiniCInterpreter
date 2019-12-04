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
		self.array_of_arrays = [(True, 0, []) for i in range(0)]
		self.top = BASE

	# Handles frame to reflect scope for a new bracket
	def into_bracket(self):
		self.symbol_tables.append(SymbolTable())

	# Handles frame to reflect scope for a new function
	def into_function(self):
		self.symbol_tables.append(None)
		self.symbol_tables.append(SymbolTable())

	# Handles frame to reflect scope after escaping from bracket
	def escape_bracket(self):
		self.symbol_tables.pop()

	# Handles frame to reflect scope after escaping from function
	def escape_function(self):
		while self.symbol_tables[-1] != None:
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
		if self.add_function(name, function):
			return Ok()
		else:
			return Err()

	# Returns corresponding functioin
	def get_function(self, name):
		entry = self.search_function(name)
		if entry:
			return Ok(entry)
		else:
			return Err()

	# Private
	# Adds a new symbol
	def add_symbol(self, name, entry):
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
	def allocate_symbol(self, is_int, length):
		rax = self.top
		self.top += 1
		self.array_of_arrays.append((is_int, length, [None for i in range(length)]))
		return rax

	# Declares corresponding symbol
	def declare_direct(self, name, line, is_int, value=None):
		actual_value = None
		if value != None:
			actual_value = int(value) if is_int else float(value)
		if self.add_symbol(name, SymbolEntry(line, is_int, False, actual_value)): return Ok()
		else: return Err()

	def declare_pointer(self, name, line, is_int, addr):
		act_is_int = self.array_of_arrays[addr][0]
		if is_int != act_is_int: return Err()
		if self.add_symbol(name, SymbolEntry(line, is_int, True, addr)): return Ok()
		else: return Err()

	def declare_array(self, name, line, is_int, length):
		addr = self.allocate_symbol(is_int, length)
		if self.add_symbol(name, SymbolEntry(line, is_int, True, addr)): return Ok()
		else: return Err()

	# Returns corresponding type
	def get_type(self, name):
		entry = self.search_symbol(name)
		if entry:
			return Ok(entry.get_type())
		else:
			return Err()

	# Returns corresponding value
	# Garbage value defaults to 0xcccc (not a bitstring though lul)
	def get_value(self, name, index = None):
		entry = self.search_symbol(name)
		if entry:
			is_int, is_pointer, value = entry.get_value()
			if index == None: return Ok((is_int, is_pointer, value if value != None else 0xcccc))
			if not is_pointer: return Err()
			# garbage value
			if index < 0 or index >= self.array_of_arrays[value][1]: return Ok((is_int, False, 0xcccc))
			return Ok((is_int, False, self.array_of_arrays[value][2][index]))
		else:
			return Err()

	def get_value_cmd(self, name, index = None):
		entry = self.search_symbol(name)
		if entry:
			is_int, is_pointer, value = entry.get_value()
			if index == None: return Ok((is_int, is_pointer, value))
			if not is_pointer: return Err()
			# garbage value
			if index < 0 or index >= self.array_of_arrays[value][1]: return Err()
			return Ok((is_int, False, self.array_of_arrays[value][2][index]))
		else:
			return Err()

	# Returns corresponding history
	# 
	def get_history(self, name):
		entry = self.search_symbol(name)
		if entry:
			return Ok(entry.get_history())
		else:
			return Err()

	# Updates corresponding value
	# Should be called after validating type with get_type?
	def update_value(self, name, line, value, index = None):
		entry = self.search_symbol(name)
		if entry:
			is_int, is_pointer, addr = entry.get_value()
			if index == None:
				if is_pointer: return Err()
				entry.update_value(line, int(value) if is_int else float(value))
				return Ok()
			if not is_pointer: return Err()
			# idk if it is important
			if index < 0 or index >= self.array_of_arrays[addr][1]: return Ok()
			self.array_of_arrays[addr][2][index] = int(value) if is_int else float(value)
			return Ok()
		else:
			return Err()
