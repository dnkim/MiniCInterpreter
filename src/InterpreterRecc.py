from Frame import Frame
from Command import Command, CmdException
from Result import *
from LexicalStep import Lex
from ParsingStep import Par
from ParsedItems import ParsedFactor2, ParsedExpr1
from ParseEnum import *
from LexicalStep import sub_count, sub_isn_spch
import sys

MAIN = "main"
MAX_DEPTH = 50000

class RTException(Exception): pass

class ReturnException(Exception): pass

class IInt:
	def __init__(self, num):
		self.num = int(num)

class IFlt:
	def __init__(self, num):
		self.num = float(num)

class IAdd:
	def __init__(self, num):
		self.num = num

class FakeParsedItem:
    def __init__(self, func, call, back_ttf, mainmain=False):
        self.type = PitFF
        self.stuff = [func, call, back_ttf, mainmain]

class FakeParsedIte2:
    def __init__(self, arguments, line_num):
        self.type = PitPtF
        self.stuff = [arguments, line_num]

class InterpreterRecc:
    def __init__(self, goal, test = False, actual_code_lines = [], no_command = True):
        sys.setrecursionlimit(10000)
        self.test = test
        self.actual_code_lines = actual_code_lines
        self.no_command = no_command
        self.frame = Frame()
        self.command = Command(self.frame, self.no_command, self.actual_code_lines)
        self.func_depth = {}
        self.proper_exit = False
        self.exit_code = -1
        self.states = []
        self.stuffs = []

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

    def handle_func(self, func):
        self.test_Err(self.frame.declare_function(func.name, func), func.line_num, "Already function with that name")
        self.func_depth[func.name] = 0

    def handle_goal(self, goal):
        for func in goal.funcs:
            self.handle_func(func)

        main = self.frame.get_function(MAIN)
        main = self.test_Err(main, len(self.actual_code_lines), "Found no main()")
        self.test_something(len(main.arguments) == 0, main.line_num, "main() should have no arguments for our stupid implementation")

        self.exit_code = int(self.doit(main).num)
        self.proper_exit = True

    def beginners_luck(self, pi):
        tt = pi.type
        self.states.append(tt)
        if tt < 13:
            if tt < 10:
                if tt < 7:
                    if tt < 4:
                        if tt == PitStmt2: #forst (forst, init=3/cond=0/stmt=1/update=2, init'd)
                            self.stuffs.append([pi, 3, False])
                        else: #PitStmt3 ifst (ifst, calcd_cond, ran_stmt)
                            self.stuffs.append([pi, False, False])
                    elif tt == PitStmt4: #cmpdst (stmt4, next_stmt)
                        self.stuffs.append([pi, 0])
                    else: #PitStmt5 retst (retst, calcd_return_value)
                        self.stuffs.append([pi, False])
                elif tt < 9:
                    if tt == PitDecl:
                        self.stuffs.append([pi])
                    else: #PitInst3 expr
                        self.stuffs.append([pi])
                else: #PitInst4 noop
                    self.stuffs.append([pi])
            elif tt < 12:
                if tt == PitExpr1: #arithmetic, (expr1, lhs, last_index)
                    #rax = IInt(0)
                    self.stuffs.append([pi, IInt(0), 0])
                else: #PitExpr2 assignment (expr2, calcd_rhs, calcd_index, index)
                    self.stuffs.append([pi, False, False, 0])
            else: #PitTerm (term, lhs, last_index)
                #rax = IInt(1)
                self.stuffs.append([pi, IInt(1), 0])
        elif tt < 16:
            if tt < 15:
                if tt == PitFactor1: #lhs/++lhs/lhs++
                    self.stuffs.append([pi, False])
                else: #PitFactor2 function call, (factor2, args_done, calc'd_args, back_ttf, func)
                    self.stuffs.append([pi, 0, [], 0, None])
            else: #PitFactor3 int
                self.stuffs.append([pi])
        elif tt < 18:
            if tt == PitFactor4: #float
                self.stuffs.append([pi])
            else: #PitFactor5 (expr)
                self.stuffs.append([pi])
        elif tt == PitFactor6: #unary +/- (factor6, calcd)
            self.stuffs.append([pi, False])
        elif tt == PitFF: #execute function??
            self.stuffs.append(pi.stuff+[0])
        else: #(0arguments, 1line_num, 2formatted, 3next_index, 4how_to_print, 5string_blocks, 6arg_values, 7done)
            self.stuffs.append(pi.stuff+[False, 1, [], [], [], False])
            

    def doit(self, main):
        rax = IInt(0xcccc)
        self.frame.into_function()
        self.beginners_luck(FakeParsedItem(main, [], 0, True))
        self.command.skip_lines(main.line_num, True)

        while True:
            exe = self.stuffs[-1]
            tt = self.states[-1]
            try:
                if tt < 13:
                    if tt < 10:
                        if tt < 7:
                            if tt < 4:
                                if tt == PitStmt2: #(forst, init=3/cond=0/stmt=1/update=2, init'd)
                                    if exe[1] == 0:
                                        if rax.num != 0:
                                            exe[1] = 1
                                            self.beginners_luck(exe[0].stmt)
                                            continue
                                        
                                        forst = exe[0]
                                        to_line = forst.stmt.end_ln if forst.stmt.type == PitStmt4 else forst.stmt.line_num
                                        self.command.skip_lines(to_line)
                                        self.frame.escape_bracket()
                                        self.states.pop()
                                        self.stuffs.pop()
                                        continue
                                    
                                    elif exe[1] == 1:
                                        exe[1] = 2
                                        self.command.skip_lines(exe[0].line_num, True)
                                        self.beginners_luck(exe[0].update)
                                        continue
                                    elif exe[1] == 2:
                                        exe[1] = 0
                                        self.beginners_luck(exe[0].condition)
                                        continue
                                    elif exe[2]:
                                        exe[1] = 0
                                        self.beginners_luck(exe[0].condition)
                                        continue
                                    else:
                                        exe[2] = True
                                        self.command.feed_line(exe[0].line_num)
                                        self.frame.into_bracket()
                                        self.beginners_luck(exe[0].initialize)
                                        continue

                                else: #PitStmt3 ifst (stmts, calcd_cond, ran_stmt)
                                    if not exe[1]:
                                        self.command.feed_line(exe[0].line_num)
                                        exe[1] = True
                                        self.beginners_luck(exe[0].condition)
                                        continue

                                    if not exe[2]:
                                        exe[2] = True
                                        if rax.num != 0:
                                            self.beginners_luck(exe[0].stmt)
                                            continue
                                    
                                    ifst = exe[0]
                                    to_line = ifst.stmt.end_ln if ifst.stmt.type == PitStmt4 else ifst.stmt.line_num
                                    self.command.skip_lines(to_line)
                                    self.states.pop()
                                    self.stuffs.pop()
                                    continue
                            
                            elif tt == PitStmt4: #cmpdst (stmts, next_stmt)
                                if exe[1] == 0:
                                    self.command.feed_line(exe[0].line_num)
                                    self.frame.into_bracket()
                                try:
                                    stmt = exe[0].stmts[exe[1]]
                                    self.beginners_luck(stmt)
                                    exe[1] = exe[1] + 1
                                    continue
                                except IndexError:
                                    pass
                                
                                self.frame.escape_bracket()
                                self.command.feed_line(exe[0].end_ln)
                                self.states.pop()
                                self.stuffs.pop()
                                continue

                            
                            else: #PitStmt5 retst = exe[0], calcd = exe[1]
                                if not exe[1]:
                                    exe[1] = True
                                    self.command.feed_line(exe[0].line_num)
                                    self.beginners_luck(exe[0].expr)
                                    continue
                                raise ReturnException()

                        elif tt < 9:
                            if tt == PitDecl:
                                decl = exe[0]
                                self.command.feed_line(decl.line_num)
                                for thing in decl.declarations:
                                    if thing[1] == None:
                                        result = self.frame.declare_direct(thing[0], decl.line_num, decl.declares_int)
                                        self.test_Err(result, decl.line_num, "Declaration went wrong")
                                        continue
                                    result = self.frame.declare_array(thing[0], decl.line_num, decl.declares_int, thing[1])
                                    self.test_Err(result, decl.line_num, "Declaration went wrong")
                                
                                self.states.pop()
                                self.stuffs.pop()
                                continue
                            
                            else: #PitInst3 expr
                                self.command.feed_line(exe[0].line_num)
                                self.states.pop()
                                self.stuffs.pop()
                                self.beginners_luck(exe[0].expr)
                                continue
                        
                        else: #PitInst4 noop
                            self.command.feed_line(exe[0].line_num)
                            self.states.pop()
                            self.stuffs.pop()
                            continue
                    
                    elif tt < 12:
                        if tt == PitExpr1: #arithmetic expr1 = exe[0], lhs = exe[1], next_index = exe[2]
                            expr1 = exe[0]
                            if exe[2] != 0:
                                lhs, rhs = exe[1], rax
                                op = expr1.terms_and_ops[exe[2]-3]
                                self.test_something(not isinstance(lhs, IAdd), expr1.line_num, "Pointer arithmetic")
                                lhn, rhn = lhs.num, rhs.num
                                if op == 0: result = lhn + rhn
                                elif op == 1: result = lhn - rhn
                                elif op == 2: result = 1 if (lhn > rhn) else 0
                                else: result = 1 if (lhn < rhn) else 0
                                if isinstance(rhs, IAdd):
                                    exe[1] = IAdd(result)
                                elif isinstance(lhs, IFlt) or isinstance(rhs, IFlt):
                                    exe[1] = IFlt(result)
                                else:
                                    exe[1] = IInt(result)

                            if exe[2] == 0 or op < 2:
                                try:
                                    next_term = expr1.terms_and_ops[exe[2]]
                                    next_op = expr1.terms_and_ops[exe[2]-1]
                                    exe[2] = exe[2] + 2
                                    if next_op < 2:
                                        self.beginners_luck(next_term)
                                        continue
                                    pexpr = ParsedExpr1(expr1.line_num)
                                    pexpr.terms_and_ops = expr1.terms_and_ops[exe[2]-2:]
                                    self.beginners_luck(pexpr)
                                    
                                    continue
                                except IndexError:
                                    pass
                            
                            rax = exe[1]
                            self.states.pop()
                            self.stuffs.pop()
                            continue
                            
                        else: #PitExpr2 assignment, expr2 = exe[0], calcd_rhs = exe[1], calcd_actual_index = exe[2], actual_index = exe[3]
                            expr2 = exe[0]
                            name, index = expr2.lhs
                            if not exe[2]:
                                exe[2] = True
                                if index != None:
                                    self.beginners_luck(index)
                                    continue
                            
                            if not exe[1]:
                                if index != None:
                                    self.test_something(not isinstance(rax, IFlt), index.line_num, "Float index to array")
                                    exe[3] = rax.num

                                exe[1] = True
                                self.beginners_luck(expr2.expr)
                                continue
                            
                            if index != None:
                                index = exe[3]
                            is_int, is_pointer = self.test_Err(self.frame.get_type(name), expr2.line_num, "No such symbol maybe?")
                            rhs = rax
                            if not isinstance(rhs, IAdd):
                                self.test_Err(self.frame.update_value(name, expr2.line_num, rhs.num, index), expr2.line_num, "Idk probably index out of bounds")
                                rax = IInt(rhs.num) if is_int else IFlt(rhs.num)
                            elif is_pointer and index == None:
                                self.test_Err(self.frame.update_value(name, expr2.line_num, rhs.num), expr2.line_num, "Probably because I disabled pointer assignment as well")
                                rax = rhs		
                            else:
                                self.report_rt_err(expr2.line_num, "Hmm probably symbol didn't exist or assigned pointer to non pointer")

                            self.states.pop()
                            self.stuffs.pop()
                            continue
                    
                    else: #PitTerm, term = exe[0], lhs = exe[1], next_index = exe[2]
                        
                        # This explicitly bans pointer arithmetic forever
                        term = exe[0]
                        if exe[2] != 0:
                            lhs, rhs = exe[1], rax
                            self.test_something(not isinstance(lhs, IAdd), term.line_num, "Pointer arithmetic")
                            lhn, rhn = lhs.num, rhs.num
                            op = term.factors_and_ops[exe[2]-3]
                            if op == 0: result = lhn * rhn
                            else: result = lhn / rhn if rhn != 0 else self.report_rt_err(term.line_num, "Zero division")
                            if isinstance(rhs, IAdd):
                                exe[1] = IAdd(result)
                            elif isinstance(lhs, IFlt) or isinstance(rhs, IFlt):
                                exe[1] = IFlt(result)
                            else:
                                exe[1] = IInt(result)
                            
                        try:
                            next_factor = term.factors_and_ops[exe[2]]
                            exe[2] = exe[2] + 2
                            self.beginners_luck(next_factor)
                            continue
                        except IndexError:
                            pass
                        
                        rax = exe[1]
                        self.states.pop()
                        self.stuffs.pop()
                        continue
                
                elif tt < 16:
                    if tt < 15:
                        if tt == PitFactor1: #lhs/++lhs/lhs++ (factor1, calcd_real_index)
                            factor1 = exe[0]
                            name, index = factor1.lhs
                            if not exe[1]:
                                exe[1] = True
                                if index != None:
                                    self.beginners_luck(index)
                                    continue
                            
                            if index != None:
                                self.test_something(not isinstance(rax, IFlt), index.line_num, "Float index to array")
                                index = rax.num
                            is_int, is_pointer, value = self.test_Err(self.frame.get_value(name, index), factor1.line_num, "No such symbol or something")
                            value = 0 if value == None else value

                            op = factor1.op
                            if op == 0:
                                if is_pointer:
                                    rax = IAdd(value)
                                else:
                                    rax = IInt(value) if is_int else IFlt(value)
                            
                            else:
                                self.test_something(not is_pointer, factor1.line_num, "Pointer increment")
                                self.frame.update_value(name, factor1.line_num, value + 1, index)
                                raxv = value + 1 if op == 1 else value
                                rax = IInt(raxv) if is_int else IFlt(raxv)
                            
                            self.states.pop()
                            self.stuffs.pop()
                            continue
                        
                        else: #PitFactor2 (factor2, args_done, calcd_args, bttf, func)
                            args_done = exe[1]
                            factor2 = exe[0]
                            if args_done > 0:
                                exe[2].append(rax)
                                if args_done < len(factor2.call):
                                    self.beginners_luck(factor2.call[args_done])
                                    exe[1] = exe[1] + 1
                                    continue

                            else:
                                self.test_something(isinstance(self.frame.get_type(factor2.func_name), Err), factor2.line_num, "Not a function in this scope")
                                func = self.frame.get_function(factor2.func_name)
                                if isinstance(func, Err):
                                    self.test_something(factor2.func_name == "printf", factor2.line_num, "No such function")
                                    #handle printf
                                    somethin2 = FakeParsedIte2(factor2.call, factor2.line_num)
                                    self.states.pop()
                                    self.stuffs.pop()
                                    self.beginners_luck(somethin2)
                                    continue
                                
                                func = func.value
                                exe[4] = func
                                exe[3] = self.command.current_line
                                self.command.skip_lines(func.start_ln, True)
                                if len(func.arguments) != len(factor2.call):
                                    self.report_rt_err(func.line_num, "Function call argument length mismatch")

                                if len(func.arguments) > 0:
                                    self.beginners_luck(factor2.call[0])
                                    exe[1] = 1
                                    continue
                            
                            func = exe[4]
                            arg_values = exe[2]
                            self.frame.into_function()
                            self.func_depth[factor2.func_name] += 1
                            if self.func_depth[factor2.func_name] > MAX_DEPTH:
                                self.report_rt_err(factor2.line_num, "Max function recursion depth "+str(MAX_DEPTH)+" reached for "+factor2.func_name)
                            #rax = IInt(0) if func.returns_int else IFlt(0)
                            for i in range(len(func.arguments)):
                                is_int, is_pointer, arg_name = func.arguments[i]
                                num = arg_values[i].num
                                if is_pointer and isinstance(arg_values[i], IAdd):
                                    result = self.frame.declare_pointer(arg_name, func.line_num, is_int, num)
                                    self.test_Err(result, func.line_num, "Pointer argument error")
                                elif not is_pointer and not isinstance(arg_values[i], IAdd):
                                    result = self.frame.declare_direct(arg_name, func.line_num, is_int, num)
                                    self.test_Err(result, func.line_num, "Non-pointer argument error")
                                else:
                                    print(is_pointer, isinstance(arg_values[i], IAdd))
                                    self.report_rt_err(func.line_num, "Argument type mismatch")

                            something = FakeParsedItem(exe[4], exe[2], exe[3])
                            self.states.pop()
                            self.stuffs.pop()
                            self.beginners_luck(something)
                            continue
                            
                    else: #PitFactor3 int
                        rax = IInt(exe[0].num)
                        self.states.pop()
                        self.stuffs.pop()
                        continue
                
                elif tt < 18:
                    if tt == PitFactor4: #float
                        rax = IFlt(exe[0].num)
                        self.states.pop()
                        self.stuffs.pop()
                        continue
                    
                    else: #PitFactor5 (expr)
                        factor5 = exe[0]
                        self.states.pop()
                        self.stuffs.pop()
                        self.beginners_luck(factor5.expr)
                        continue
                
                elif tt == PitFactor6: #unary +/-
                    factor6 = exe[0]
                    if exe[1]:
                        inum = rax
                        self.test_something(not isinstance(inum, IAdd), factor6.line_num, "Pointer unary op")
                        inum.num = inum.num if factor6.op == 0 else -inum.num
                        rax = inum

                        self.states.pop()
                        self.stuffs.pop()
                        continue
                    exe[1] = True
                    self.beginners_luck(factor6.factor)
                    continue
                
                elif tt == PitFF: #execute function (func, call, bttf, mainmain, executed)
                    try:
                        stmt = exe[0].stmts[exe[4]]
                        self.beginners_luck(stmt)
                        exe[4] = exe[4] + 1
                        continue
                    except IndexError:
                        pass
                    
                    self.command.feed_line(exe[0].end_ln)
                    raise ReturnException()

                else: #execute printf (0arguments, 1line_num, 2formatted, 3next_index, 4how_to_print, 5string_blocks, 6arg_values, 7done)
                    arguments = exe[0]
                    line_num = exe[1]
                    if exe[7]:
                        how_to_print = exe[4]
                        string_blocks = exe[5]
                        arg_values = exe[6]

                        string = string_blocks[0]
                        for i in range(len(how_to_print)):
                            if how_to_print[0]:
                                string = string + str(int(arg_values[i].num))
                            else:
                                string = string + str(float(arg_values[i].num))
                            string = string + string_blocks[i + 1]

                        print(string, end='')
                        rax = IInt(len(string))
                        self.states.pop()
                        self.stuffs.pop()
                        continue
                    
                    elif exe[2]:
                        exe[6].append(rax)
                        next_index = exe[3]
                        if next_index < len(arguments):
                            exe[3] = exe[3] + 1
                            arg = arguments[next_index]
                            self.test_something(not isinstance(arg, str), line_num, "Non primary string argument for printf")
                            self.beginners_luck(arg)
                            continue
                        exe[7] = True
                        continue

                    else:
                        exe[2] = True
                        self.test_something(len(arguments) > 0, line_num, "Too few arguments to printf")
                        self.test_something(isinstance(arguments[0], str), line_num, "Non string first arg to printf")

                        i = 0
                        top = arguments[0]
                        l = len(top)
                        how_to_print = []
                        string_blocks = [top]
                        while True:
                            
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
                        exe[4] = how_to_print
                        exe[5] = string_blocks
                        if len(arguments) > 1:
                            exe[3] = exe[3] + 1
                            arg = arguments[1]
                            self.test_something(not isinstance(arg, str), line_num, "Non primary string argument for printf")
                            self.beginners_luck(arg)
                        else:
                            exe[7] = True
                        continue


            except ReturnException:
                while self.states[-1] != PitFF:
                    self.states.pop()
                    self.stuffs.pop()
                exe = self.stuffs[-1]
                func = exe[0]

                if not exe[3]:
                    self.frame.escape_function()
                    self.command.skip_lines(exe[2])

                self.func_depth[func.name] -= 1
                rax = IInt(rax.num) if func.returns_int else IFlt(rax.num)
                self.states.pop()
                self.stuffs.pop()
                if len(self.states) == 0:
                    break
        
        return rax
