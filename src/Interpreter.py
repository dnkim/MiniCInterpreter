from Frame import Frame
from Command import Command, CmdException
from Result import *
from LexicalStep import Lex
from ParsingStep import Par
from ParsedItems import ParsedFactor2
from ParseEnum import *
from LexicalStep import sub_count, sub_isn_spch
import sys

MAIN = "main"

class RTException(Exception): pass

class ReturnException(Exception):
	def __init__(self, Inum):
		self.Inum = Inum
		super(ReturnException, self).__init__("Returning something")

class IInt:
	def __init__(self, num):
		self.num = int(num)

class IFlt:
	def __init__(self, num):
		self.num = float(num)

class IAdd:
	def __init__(self, num):
		self.num = num

class Interpreter:
	def __init__(self, goal, test = False, actual_code_lines = [], no_command = True):
		self.test = test
		self.actual_code_lines = actual_code_lines
		self.no_command = no_command
		self.frame = Frame()
		self.command = Command(self.frame, self.no_command, self.actual_code_lines)
		self.proper_exit = False
		self.exit_code = -1
		self.match = {
			PitStmt2: self.handle_stmt2,
			PitStmt3: self.handle_stmt3,
			PitStmt4: self.handle_stmt4,
			PitStmt5: self.handle_stmt5,
			PitDecl: self.handle_decl,
			PitInst3: self.handle_inst3,
			PitInst4: self.handle_inst4,
			PitExpr1: self.handle_expr1,
			PitExpr2: self.handle_expr2,
			PitTerm: self.handle_term,
			PitFactor1: self.handle_factor1,
			PitFactor2: self.handle_factor2,
			PitFactor3: self.handle_factor3,
			PitFactor4: self.handle_factor4,
			PitFactor5: self.handle_factor5,
			PitFactor6: self.handle_factor6
		}

		try:
			self.handle_goal(goal)
			if self.proper_exit:
				print("... Program finished with exit code:", self.exit_code)
			while not self.no_command:
				self.command.command()
		except RTException:
			pass
		except CmdException:
			pass

	def report_rt_err(self, line_num, string):
		if self.test:
			print("At line ", line_num, ", ", string, ", SmileyFace", sep='')
			print(self.actual_code_lines[line_num - 1])
		else:
			print("Run-time error : line", line_num)
		raise RTException

	def test_something(self, to_test, line_num, string):
		if to_test: return
		self.report_rt_err(line_num, string)
		assert(False)

	def test_Err(self, to_test, line_num, string):
		self.test_something(not isinstance(to_test, Err), line_num, string)
		return to_test.value

	def handle_goal(self, goal):
		for func in goal.funcs:
			self.handle_func(func)

		main = self.frame.get_function(MAIN)
		main = self.test_Err(main, len(self.actual_code_lines), "Found no main()")
		self.test_something(len(main.arguments) == 0, main.line_num, "main() should have no arguments for our stupid implementation")

		self.exit_code = int(self.execute_func(main, [], True).num)
		self.proper_exit = True
		
	def execute_func(self, func, arguments, mainmain = False):
		back_ttf = self.command.current_line
		self.command.skip_lines(func.start_ln, True)
		if len(func.arguments) != len(arguments):
			self.report_rt_err(func.line_num, "Function call argument length mismatch")
		
		arg_values = []
		for arg in arguments:
			self.test_something(not isinstance(arg, str), func.line_num, "String argument for non printf function call")
			arg_values.append(self.whos_that_poke(arg))

		self.frame.into_function()
		rax = IInt(0) if func.returns_int else IFlt(0)
		for i in range(len(arguments)):
			is_int, is_pointer, arg_name = func.arguments[i]
			num = arg_values[i].num
			if is_pointer and isinstance(arg_values[i], IAdd):
				result = self.frame.declare_pointer(arg_name, func.line_num, is_int, num)
				self.test_Err(result, func.line_num, "Pointer argument error")
			elif not is_pointer and not isinstance(arg_values[i], IAdd):
				result = self.frame.declare_direct(arg_name, func.line_num, is_int, num)
				self.test_Err(result, func.line_num, "Non-pointer argument error")
			else: 
				self.report_rt_err(func.line_num, "Argument type mismatch")

		for stmt in func.stmts:
			try:
				self.whos_that_poke(stmt)
			except ReturnException as RE:
				rax = RE.Inum
				if isinstance(rax, IAdd):
					self.report_rt_err(stmt.line_num, "Returning pointer")
				rax = IInt(rax.num) if func.returns_int else IFlt(rax.num)
				break
		
		if stmt.type != PitStmt5:
			self.command.feed_line(func.end_ln)

		if not mainmain:
			self.frame.escape_function()
			self.command.skip_lines(back_ttf)
		return rax
	
	def execute_printf(self, arguments, line_num):
		self.test_something(len(arguments) > 0, line_num, "Too few arguments to printf")
		self.test_something(isinstance(arguments[0], str), line_num, "Non string first arg to printf")

		i = 0
		top = arguments[0]
		l = len(top)
		how_to_print = []
		string_blocks = [top]
		while True:
			#print(i, l, string_blocks, top)
			i = sub_count(top, sub_isn_spch, l, i)
			if i == l: break
			if top[i] == '\\':
				if top[i+1] == 'n': top = top[:i] + '\n' + top[i+2:]
				elif top[i+1] == '\\': top = top[:i] + '\\' + top[i+2:]
				else: self.report_rt_err(line_num, "undefined use of \\")
				i = i + 1
				l = l - 1
				string_blocks[-1] = top
			elif top[i] == '%':
				if top[i+1] == '%':
					top = top[:i] + '%' + top[i+2:]
					i = i + 1
					l = l - 1
					string_blocks[-1] = top
					continue
				if top[i+1] == 'd' or top[i+1] == 'f':
					how_to_print.append(top[i+1] == 'd')
					top_left = top[:i]
					top = top[i+2:]
					l = l - i - 2
					i = 0
					string_blocks[-1] = top_left
					string_blocks.append(top)
				else: self.report_rt_err(line_num, "undefined use of %")
		self.test_something(len(how_to_print) == len(arguments) - 1, line_num, "printf format argument mismatch")
		
		arg_values = []
		for arg in arguments[1:]:
			self.test_something(not isinstance(arg, str), line_num, "Non primary string argument for printf")
			arg_values.append(self.whos_that_poke(arg))

		string = string_blocks[0]
		for i in range(len(how_to_print)):
			if how_to_print[0]:
				string = string + str(int(arg_values[i].num))
			else:
				string = string + str(float(arg_values[i].num))
			string = string + string_blocks[i + 1]

		print(string, end='')
		return IInt(len(string))


	def whos_that_poke(self, parseditem):
		function = self.match[parseditem.type]
		return function(parseditem)

	def handle_func(self, func):
		self.test_Err(self.frame.declare_function(func.name, func), func.line_num, "Already function with that name")

	# For Stmt
	def handle_stmt2(self, forst):
		self.command.feed_line(forst.line_num)
		self.frame.into_bracket()
		
		self.whos_that_poke(forst.initialize)
		while int(self.whos_that_poke(forst.condition).num):
			self.whos_that_poke(forst.stmt)
			self.command.skip_lines(forst.line_num, True)
			self.whos_that_poke(forst.update)

		to_line = forst.stmt.end_ln if forst.stmt.type == PitStmt4 else forst.stmt.line_num
		self.command.skip_lines(to_line)
		self.frame.escape_bracket()

	# If Stmt
	def handle_stmt3(self, ifst):
		self.command.feed_line(ifst.line_num)
		if int(self.whos_that_poke(ifst.condition).num):
			self.whos_that_poke(ifst.stmt)

		to_line = ifst.stmt.end_ln if ifst.stmt.type == PitStmt4 else ifst.stmt.line_num
		self.command.skip_lines(to_line)

	# Compound Stmt i.e. {stmt/decl*}
	def handle_stmt4(self, stmts):
		self.command.feed_line(stmts.line_num)
		self.frame.into_bracket()

		for stmt in stmts.stmts:
			self.whos_that_poke(stmt)

		self.frame.escape_bracket()
		self.command.feed_line(stmts.end_ln)

	# Return Stmt
	def handle_stmt5(self, retst):
		self.command.feed_line(retst.line_num)
		raise ReturnException(self.whos_that_poke(retst.expr))

	# Declaration
	def handle_decl(self, decl):
		self.command.feed_line(decl.line_num)
		for thing in decl.declarations:
			if thing[1] == None:
				result = self.frame.declare_direct(thing[0], decl.line_num, decl.declares_int)
				self.test_Err(result, decl.line_num, "Declaration went wrong")
				continue
			result = self.frame.declare_array(thing[0], decl.line_num, decl.declares_int, thing[1])
			self.test_Err(result, decl.line_num, "Declaration went wrong")


	# Inst3 : Expr
	def handle_inst3(self, inst3):
		self.command.feed_line(inst3.line_num)
		self.whos_that_poke(inst3.expr)

	# Inst4 : Noop
	def handle_inst4(self, inst4):
		self.command.feed_line(inst4.line_num)

	def sub_do_arithmetic(self, lhs, rhs, op, line_num):
		self.test_something(not (isinstance(lhs, IAdd) or isinstance(rhs, IAdd)), line_num, "Pointer arithmetic")
		lhn, rhn = lhs.num, rhs.num
		result = 0
		if op == 0: result = lhn + rhn
		elif op == 1: result = lhn - rhn
		elif op == 2: result = 1 if (lhn > rhn) else 0
		else: result = 1 if (lhn < rhn) else 0
		if isinstance(lhs, IFlt) or isinstance(rhs, IFlt):
			return IFlt(result)
		else:
			return IInt(result)

	def do_arithmetic(self, tao):
		lhs = self.whos_that_poke(tao[0])
		l = (len(tao) - 1) // 2
		for i in range(l):
			op = tao[1 + 2 * i]
			if op > 1:
				rhs = self.do_arithmetic(tao[2 + 2 * i:])
				return self.sub_do_arithmetic(lhs, rhs, op, tao[0].line_num)
			else:
				rhs = self.whos_that_poke(tao[2 + 2 * i])
				lhs = self.sub_do_arithmetic(lhs, rhs, op, tao[0].line_num)
		
		return lhs

	# Expr1 : Arithmetic
	def handle_expr1(self, expr1):
		return self.do_arithmetic(expr1.terms_and_ops)

	def get_actual_index(self, index):
		if index != None:
			line_num = index.line_num
			index = self.whos_that_poke(index)
			self.test_something(not isinstance(index, IFlt), line_num, "Float index to array")
			# a rare implicit cast of pointer to int
			index = index.num
		return index

	# Expr2 : Assignment
	def handle_expr2(self, expr2):
		name, index = expr2.lhs
		index = self.get_actual_index(index)

		is_int, is_pointer = self.test_Err(self.frame.get_type(name), expr2.line_num, "No such symbol maybe?")
		rhs = self.whos_that_poke(expr2.expr)
		if not isinstance(rhs, IAdd):
			self.test_Err(self.frame.update_value(name, expr2.line_num, rhs.num, index), expr2.line_num, "Idk probably index out of bounds")
			return IInt(rhs.num) if is_int else IFlt(rhs.num)
		if is_pointer and index == None:
			self.test_Err(self.frame.update_value(name, expr2.line_num, rhs.num), expr2.line_num, "Probably because I disabled pointer assignment as well")
			return rhs		
		self.report_rt_err(expr2.expr, "Hmm probably symbol didn't exist or assigned pointer to non pointer")

	def sub_do_products(self, lhs, rhs, op, line_num):
		self.test_something(not (isinstance(lhs, IAdd) or isinstance(rhs, IAdd)), line_num, "Pointer arithmetic")
		lhn, rhn = lhs.num, rhs.num
		result = 0
		if op == 0: result = lhn * rhn
		else: result = lhn / rhn if rhn != 0 else self.report_rt_err(line_num, "Zero division")
		if isinstance(lhs, IFlt) or isinstance(rhs, IFlt):
			return IFlt(result)
		else:
			return IInt(result)

	def do_products(self, fao):
		lhs = self.whos_that_poke(fao[0])
		l = (len(fao) - 1) // 2
		for i in range(l):
			op = fao[1 + 2 * i]
			rhs = self.whos_that_poke(fao[2 + 2 * i])
			lhs = self.sub_do_products(lhs, rhs, op, fao[0].line_num)
		
		return lhs

	# Term
	def handle_term(self, term):
		return self.do_products(term.factors_and_ops)

	# Factor1 : lhs / ++lhs / lhs++
	def handle_factor1(self, factor1):
		name, index = factor1.lhs
		index = self.get_actual_index(index)

		is_int, is_pointer, value = self.test_Err(self.frame.get_value(name, index), factor1.line_num, "No such symbol or something")
		value = 0 if value == None else value
		op = factor1.op
		if op == 0:
			if is_pointer:
				return IAdd(value)
			return IInt(value) if is_int else IFlt(value)
		
		self.test_something(not is_pointer, factor1.line_num, "Pointer increment")
		self.frame.update_value(name, factor1.line_num, value + 1, index)
		rax = value + 1 if op == 1 else value
		return IInt(rax) if is_int else IFlt(rax)

	# Factor2 : Function call
	def handle_factor2(self, factor2):
		self.test_something(isinstance(self.frame.get_type(factor2.func_name), Err), factor2.line_num, "Not a function in this scope")
		func = self.frame.get_function(factor2.func_name)
		if isinstance(func, Err):
			self.test_something(factor2.func_name == "printf", factor2.line_num, "No such function")
			return self.execute_printf(factor2.call, factor2.line_num)

		func = func.value
		return self.execute_func(func, factor2.call)

	# Factor3 : Integer
	def handle_factor3(self, factor3):
		return IInt(factor3.num)

	# Factor4 : Float
	def handle_factor4(self, factor4):
		return IFlt(factor4.num)

	# Factor5 : (Expr)
	def handle_factor5(self, factor5):
		return self.whos_that_poke(factor5.expr)

	# Factor6: Unary +/- Factor
	def handle_factor6(self, factor6):
		inum = self.whos_that_poke(factor6.factor)
		self.test_something(not isinstance(inum, IAdd), factor6.line_num, "Pointer unary op")
		inum.num = inum.num if factor6.op == 0 else -inum.num
		return inum

def main():
	if len(sys.argv) < 2:
		print("Not given C program to interpret")
		return
	file_name = sys.argv[1]
	with open(file_name) as file_inp:
		lex = Lex(file_inp, True)
		par = Par(lex)
		goal = par.jobsworth()
		if goal == False:
			return
		file_inp.seek(0)
		actual_code_lines = [line.rstrip() for line in file_inp]
		no_command = True if (len(sys.argv) == 3 and sys.argv[2] == "test") else False
		interp = Interpreter(goal, True, actual_code_lines, no_command)

if __name__ == "__main__":
    main()
