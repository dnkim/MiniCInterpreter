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
		if !check_name(name):
			raise ValueError
		result = self.frame.get_value(name)
		if type(result) is Ok:
			if result.value is None:
				value = "N/A"
			else:
				value = str(result.value)
			print(value)
		else:
			print("Invisible variable")

	def cmd_trace(self, name):
		if !check_name(name):
			raise ValueError:
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
	if not name[0].isalpha():
		return False
	for c in name[1:]:
		if not (c.isalpha() or c.isdecimal() or ch == "_"):
			return False
	return True
