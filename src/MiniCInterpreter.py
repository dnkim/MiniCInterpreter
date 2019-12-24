from LexicalStep import Lex
from ParsingStep import Par
from Interpreter import Interpreter
from InterpreterRecc import InterpreterRecc
import sys

def main():
	if len(sys.argv) < 2:
		print("Incorrect command usage")
		return
	test, recc = False, False
	for opt in sys.argv[1:-1]:
		if opt == "-t" and not test:
			test = True
		elif opt == "-r" and not recc:
			recc = True
		else:
			print("Incorrect command usage")
			return
	file_name = sys.argv[len(sys.argv) - 1]
	with open(file_name) as file_inp:
		lex = Lex(file_inp, True)
		par = Par(lex)
		goal = par.jobsworth()
		if not goal:
			return
		file_inp.seek(0)
		actual_code_lines = [line.rstrip() for line in file_inp]
		no_command = True if test else False
		Interpreter_To_Use = InterpreterRecc if recc else Interpreter
		interp = Interpreter_To_Use(goal, False, actual_code_lines, no_command)

if __name__ == "__main__":
	main()
