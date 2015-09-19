import sys
import getch
from stack import *


class output:
    def __init__(self, result, stack):
        self.result = result
        self.stack = stack


class Equality:
    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Num(Equality):
    def __init__(self, num):
        self.val = num

    def __repr__(self):
        return "Num( "+self.val+" )"

    def eval(self, stack):
        return output(float(self), stack)


class List(Equality):
    def __init__(self, *items):
        self.items = items


class Condition(Equality):
    def __init__(self, condop, val=None):
        self.condop = condop
        self.val = val

    def __repr__(self):
        return "Cond( "+self.condop+', '+str(self.val)+" )"

    def eval(self, stack):
        if self.condop == "_":
            out = self.val.eval(stack)
            return output(len(stack) == out.result, out.stack)
        elif self.condop == '#':
            out = self.val.eval(stack)
            return output(stack.peek() == out.result, out.stack)
        elif self.condop == '*':
            return output(True, stack)
        else:
            raise SyntaxError('"'+self.condop+'" is not a valid condition operator.')


class Procedure(Equality):
    def __init__(self, proc, *args):
        self.proc = proc.upper()
        self.args = args

    def __repr__(self):
        return "Proc( "+self.proc+", "+", ".join(self.args)+" )"

    def eval(self, stack):
        if self.proc in ['+', 'ADD']:
            a = stack.pop()
            b = stack.pop()
            stack.push(b+a)

        elif self.proc in ['-', 'SUB']:
            a = stack.pop()
            b = stack.pop()
            stack.push(b-a)

        elif self.proc in ['*', 'MULT']:
            a = stack.pop()
            b = stack.pop()
            stack.push(b*a)

        elif self.proc in ['/', 'DIV']:
            a = stack.pop()
            b = stack.pop()
            stack.push(b/a)

        elif self.proc in ['%', 'MOD']:
            a = stack.pop()
            b = stack.pop()
            stack.push(b % a)

        elif self.proc in ['!', 'NOT']:
            a = stack.pop()
            stack.push(not a)

        elif self.proc in [':', 'DUP']:
            a = stack.pop()
            stack.push(a)
            stack.push(a)

        elif self.proc in ['&', 'BWAND']:
            a = stack.pop()
            b = stack.pop()
            stack.push(b & a)

        elif self.proc in ['|', 'BWOR']:
            a = stack.pop()
            b = stack.pop()
            stack.push(b | a)

        elif self.proc in ['~', 'BWNOT']:
            a = stack.pop()
            stack.push(~a)

        elif self.proc in ['\\', 'SWAP']:
            a = stack.pop()
            b = stack.pop()
            stack.push(a)
            stack.push(b)

        elif self.proc in ['$', 'DROP']:
            stack.pop()

        elif self.proc in ['P', 'PUSH']:
            arg = self.args[0].eval(stack)
            stack.push(arg.result)
            stack = arg.stack

        elif self.proc in ['.', 'PUTCH']:
            print(chr(stack.pop()), end='')

        elif self.proc in [',', 'GETCH']:
            stack.push(ord(getch.getch()))

        elif self.proc in ['PRINTS']:
            popped = ''
            while popped != '\0':
                popped = stack.pop()
                print(chr(popped), end='')

        elif self.proc in ['<', 'LT']:
            a = stack.pop()
            b = stack.pop()
            stack.push(int(b < a))

        elif self.proc in ['>', 'GT']:
            a = stack.pop()
            b = stack.pop()
            stack.push(int(b > a))

        elif self.proc in [';', 'HALT']:
            sys.exit()

        return output(True, stack)


class Instructions(Equality):
    def __init__(self, *instructions):
        self.instructions = instructions

    def __repr__(self):
        return ', '.join([repr(x) for x in self.instructions])

    def eval(self, stack):
        for x in self.instructions:
            out = x.eval(stack)
        return output(True, out.stack)


class Line(Equality):
    def __init__(self, cond, instructions):
        self.cond = cond
        self.instructions = instructions

    def __repr__(self):
        return 'Line( '+repr(self.cond)+', '+repr(self.instructions)+' )'

    def eval(self, stack):
        if self.cond.eval(stack):
            out = self.instructions.eval(stack)
            stack = out.stack
        return output(True, stack)

if __name__ == '__main__':
    stack = stack([x for x in range(100, 110)])
    print(Line(Condition('*', Num('42')), Instructions(Procedure('DUP'))))
    print(Line(Condition('*', Num('42')), Instructions(Procedure('DUP'))).eval(stack).stack.__repr__())
