from Frame import Frame
from Result import *

class CmdException(Exception): pass

class Command:
	def __init__(self, frame, no_command = False, actual_code_lines = []):
		self.no_cmd = no_command
		self.frame = frame
		self.lines = 1
		self.current_line = 0
		self.actual_code_lines = actual_code_lines
		self.digits = count_digits(len(self.actual_code_lines))

	def skip_lines(self, to_line, decrement = False):
		self.current_line = to_line
		if decrement: self.lines -= 1
		while self.lines <= 0:
			self.command()

	def feed_line(self, waiting_ln):
		self.lines = self.lines - (waiting_ln - self.current_line)
		self.current_line = waiting_ln
		while self.lines <= 0:
			self.command()

	def command(self):
		if self.no_cmd:
			self.lines = 1000
			return
		while True:
			try:
				argv = input(">> ").split()
			except:
				raise CmdException()
			argc = len(argv)
			if argc == 0: continue
			if argv[0] == "next" or argv[0] == 'n':
				if argc == 1:
					self.cmd_next(1)
					break
				elif argc == 2:
					try:
						self.cmd_next(int(argv[1]))
						break
					except ValueError:
						print("Incorrect command usage : try 'next [lines]'")
				else:
					print("Incorrect command usage : try 'next [lines]'")
			elif argv[0] == "print" or argv[0] == 'p':
				if argc == 2:
					try:
						self.cmd_print(argv[1])
					except ValueError:
						print("Invalid typing of the variable name")
				else:
					print("Invalid typing of the variable name")
			elif argv[0] == "trace" or argv[0] == 't':
				if argc == 2:
					try:
						self.cmd_trace(argv[1])
					except ValueError:
						print("Invalid typing of the variable name")
				else:
					print("Invalid typing of the variable name")
			elif argv[0] == "current" or argv[0] == 'c':
				if argc == 1:
					if self.lines > 0:
						print("EOF")
					else:
						line_to_print = self.current_line + self.lines
						print(str(line_to_print).rjust(self.digits), self.actual_code_lines[line_to_print - 1])
				else:
					print("Incorrect command usage")
			elif argv[0] == "location" or argv[0] == 'l':
				if argc == 1:
					line_to_print = self.current_line + self.lines if self.lines <= 0 else -1
					for line in range(1, len(self.actual_code_lines) + 1):
						if line == line_to_print:
							print("->", str(line).rjust(self.digits), self.actual_code_lines[line - 1])
						else:
							print("  ", str(line).rjust(self.digits), self.actual_code_lines[line - 1])
				else:
					print("Incorrect command usage")
			elif argv[0] == "quit" or argv[0] == 'q':
				if argc == 1:
					raise CmdException()
				else:
					print("Incorrect command usage")
			else:
				print("Incorrect command usage")

	def cmd_next(self, lines):
		if lines < 0:
			raise ValueError
		self.lines += lines

	def cmd_print(self, name):
		proceed, symbol, index = check_name_print(name)
		#print(proceed, symbol, index)
		if not proceed:
			raise ValueError
		result = self.frame.get_value_cmd(symbol, index)
		if type(result) is Ok:
			if result.value[2] is None:
				value = "N/A"
			else:
				if result.value[1]:
					value = hex(result.value[2]*4)
				else:
					value = str(int(result.value[2])) if result.value[0] else str(float(result.value[2]))
			print(value)
		else:
			print("Invisible variable")

	def cmd_trace(self, name):
		if not check_name(name):
			raise ValueError
		result = self.frame.get_history(name)
		if type(result) is Ok:
			for (line, value) in result.value[2]:
				line = str(line)
				if value is None:
					value = "N/A"
				else:
					if result.value[1]:
						value = hex(value*4)
					else:
						value = str(int(value)) if result.value[0] else str(float(value))
				print(name, "=", value, "at line", line)
		else:
			print("Invisible variable")

def check_name(name):
	if not (name[0].isalpha() or name[0] == '_'):
		return False
	for c in name[1:]:
		if not (c.isalpha() or c.isdecimal() or c == "_"):
			return False
	return True

def check_name_print(name):
	enc_legalc = False
	enc_lbrack = False
	enc_number = False
	enc_rbrack = False

	index_start = 0
	for i in range(len(name)):
		c = name[i]
		if not enc_legalc:
			if c.isalpha() or c == "_":
				enc_legalc = True
				continue
		
		elif not enc_lbrack:
			if c.isalpha() or c.isdecimal() or c == "_":
				continue
			if c == '[':
				enc_lbrack = True
				continue

		elif not enc_number:
			if c.isdecimal():
				index_start = i
				enc_number = True
				continue

		elif not enc_rbrack:
			if c.isdecimal():
				continue
			if c == ']':
				enc_rbrack = True
				continue

		return False, None, None

	symbol = name[0 : index_start - 1] if enc_rbrack else name
	index = int(name[index_start : -1]) if enc_rbrack else None
	return True, symbol, index

def count_digits(n):
	digits = 1
	while True:
		n //= 10
		if n == 0:
			return digits
		digits += 1
