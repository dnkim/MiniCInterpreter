from Frame import Frame
from Command import Command

MAIN = "main"

class Interpreter:
	def __init__(self):
		self.frame = Frame()
		self.command = Command()

		# build AST

		self.handle_goal(goal)

	def handle_goal(self, goal):
		for func in goal.funcs:
			self.handle_func(func)

		main = self.frame.get_function(MAIN)

		# execute main

	def handle_func(self, func):
		self.frame.add_function(func.name, func)

	def handle_factor2(self, factor2);
		func = self.frame.get_function(factor2.func_name)

		frame.into_function()

		# execute func

		frame.escape_scope()
