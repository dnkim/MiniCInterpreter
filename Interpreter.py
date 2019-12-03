from Frame import Frame
from Command import Command
from Result import *

MAIN = "main"

class Interpreter:
	def __init__(self, test = False):
		self.frame = Frame()
		self.command = Command(frame, test)

		# build AST

		#self.handle_goal(goal)

	def handle_goal(self, goal):
		for func in goal.funcs:
			self.handle_func(func)

		#main = self.frame.get_function(MAIN)

		# execute main

	def handle_func(self, func):
		self.frame.add_function(func.name, func)

	# For Stmt
	def handle_stmt2(self, forst):
		pass

	# If Stmt
	def handle_stmt3(self, ifst):
		pass

	# Compound Stmt i.e. {stmt/decl*}
	def handle_stmt4(self, stmts):
		pass

	# Return Stmt
	def handle_stmt5(self, retst):
		pass

	# Declaration
	def handle_decl(self, decl):
		pass

	# Inst3 : Expr
	def handle_inst3(self, inst3):
		pass

	# Inst4 : Noop
	def handle_inst4(self, inst4):
		pass

	# Expr1 : Arithmetic
	def handle_expr1(self, expr1):
		pass

	# Expr2 : Assignment
	def handle_expr2(self, expr2):
		pass

	# Term
	def handle_term(self, term):
		pass

	# Factor1 : lhs / lhs++ / ++lhs
	def handle_factor1(self, factor1):
		pass

	# Factor2 : Function call
	def handle_factor2(self, factor2):
		#func = self.frame.get_function(factor2.func_name)

		self.frame.into_function()

		# execute func

		self.frame.escape_scope()

	# Factor3 : Integer
	def handle_factor3(self, factor3):
		pass

	# Factor4 : Float
	def handle_factor4(self, factor4):
		pass

	# Factor5 : (Expr)
	def handle_factor5(self, factor5):
		pass

	# Factor6: Unary +/- Factor
	def handle_factor6(self, factor6):
		pass
