from LexicalStep import Lex
from ParsingStep import Par
from Interpreter import Interpreter
from InterpreterRecc import InterpreterRecc
import sys

def main():
	if not (len(sys.argv) == 2 or (len(sys.argv) == 3 and sys.argv[2] == "test") or (len(sys.argv)==4 and sys.argv[3] == 'recc')):
		print("Incorrect command usage")
		return
	file_name = sys.argv[1]
	with open(file_name) as file_inp:
		lex = Lex(file_inp, True)
		par = Par(lex)
		goal = par.jobsworth()
		if not goal:
			return
		file_inp.seek(0)
		actual_code_lines = [line.rstrip() for line in file_inp]
		no_command = True if (len(sys.argv) >= 3 and sys.argv[2] == "test") else False
		Interpreter_To_Use = InterpreterRecc if (len(sys.argv) >= 4 and sys.argv[3] == 'recc') else Interpreter
		interp = Interpreter_To_Use(goal, True, actual_code_lines, no_command)

if __name__ == "__main__":
	main()
