from Frame import Frame
from Result import *

class Command:
	def __init__(self, frame, test = False):
		self.test = test
		if self.test:
			return
		self.frame = frame
		self.lines = 0

	def feed_line(self):
		if self.test:
			return
		while self.lines == 0:
			self.command()
		self.lines -= 1

	def command(self):
		while True:
			argv = input(">>").split()
			argc = argv.length()
			if argv[0] == "next":
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
			elif argv[0] == "print":
				if argc == 2:
					try:
						self.cmd_print(argv[1])
					except ValueError:
						print("Invalid typing of the variable name")
				else:
					print("Invalid typing of the variable name")
			elif argv[0] == "trace":
				if argc == 2:
					try:
						self.cmd_trace(argv[1])
					except ValueError:
						print("Invalid typing of the variable name")
				else:
					print("Invalid typing of the variable name")

	def cmd_next(self, lines):
		if lines < 0:
			raise ValueError
		self.lines = lines

	def cmd_print(self, name):
		proceed, symbol, index = check_name_print(name)
		if not proceed:
			raise ValueError
		result = self.frame.get_value(symbol, index)
		if type(result) is Ok:
			if result.value is None:
				value = "N/A"
			else:
				value = str(result.value)
			print(value)
		else:
			print("Invisible variable")

	def cmd_trace(self, name):
		if not check_name(name):
			raise ValueError
		result = self.frame.get_value(name)
		if type(result) is Ok:
			for (line, value) in result.value:
				line = str(line)
				if value is None:
					value = "N/A"
				else:
					value = str(value)
				print(name, "=", value, "at line", line, sep = " ")
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
	if not (name[0].isalpha() or name[0] == '_'):
		return False
	
	enc_legalc = False
	enc_lbrack = False
	enc_number = False
	enc_rbrack = False

	index_start = 0
	index_end = None
	for i in range(1, len(name)):
		c = name[i]
		if not enc_legalc:
			if c.isalpha() or c.isdecimal() or c == "_":
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
				index_end = i
				enc_rbrack = True
				continue

		return False, None, None

	symbol = name[0 : index_start - 1]
	index = int(name[index_start, index_end]) if enc_rbrack else None
	return True, symbol, index