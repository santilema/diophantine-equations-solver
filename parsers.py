from symbolic_classes import *

# Parsers from the lectures

result = lambda p: p[0][0]
rest   = lambda p: p[0][1]

class Parser:
    def __rshift__(self, other):
        return Seq(self, other)

    def __xor__(self, other):
        return OrElse(self, other)
    
    def parse(self, inp):
        return self.parser.parse(inp)

    def cons(x, xs):
        if type(x) == str and xs == []:
            return x
        if type(xs) == str:
            return x + xs
        return [x] + xs
    
class Seq(Parser):
    def __init__(self, parser, and_then):
        self.parser   = parser
        self.and_then = and_then

    def parse(self, inp):
        p = self.parser.parse(inp)
        if p != []:
            return self.and_then(result(p)).parse(rest(p))

        return []
    
class OrElse(Parser):
    def __init__(self, parser1, parser2):
        self.parser1 = parser1
        self.parser2 = parser2

    def parse(self, inp):
        p = self.parser1.parse(inp)
        if p != []:
            return p

        return self.parser2.parse(inp)
    
class ParseItem(Parser):
    def parse(self, inp):
        if inp == "":
            return []
        return [(inp[0], inp[1:])]
    
class Return(Parser):
    def __init__(self, x):
        self.x = x
        
    def parse(self, inp):
        return [(self.x, inp)]

class Fail(Parser):
    def parse(self, inp):
        return []
    
class ParseSome(Parser):
    def __init__(self, parser):
        self.parser = parser >> (lambda x: \
                                 (ParseSome(parser) ^ Return([])) >> (lambda xs: \
                                 Return(Parser.cons(x, xs))))
        
class ParseIf(Parser):
    def __init__(self, pred):
        self.pred   = pred
        self.parser = ParseItem() >> (lambda c: \
                                      Return(c) if self.pred(c) else Fail())
        
class ParseChar(Parser):
    def __init__(self, c):
        self.parser = ParseIf(lambda x: c == x)
        
class ParseDigit(Parser):
    def __init__(self):
        self.parser = ParseIf(lambda c: c in "0123456789")

# Parsers for the project

class ParseKeyword(Parser):
    """
    This parser is used to parse a keyword passed as a parameter

    Example:
    >>> print(result(ParseKeyword("art").parse("artificial intelligence")))
    'art'
    """
    def __init__(self, keyword):
        self.keyword = keyword
        self.parser = ParseChar(self.keyword[0]) >> (lambda x: \
                                                (ParseKeyword(self.keyword[1:]) if len(self.keyword) > 1 else Return([])) >> (lambda xs: \
                                                    Return(Parser.cons(x, xs))))
        
class ParseDiophantine(ParseKeyword, ParseChar, ParseKeyword, ParseId):
    def __init__(self, text):
        self.text = text
        self.ws_p = ParseChar(" ")
        self.lp_p = ParseChar("(")
        self.rp_p = ParseChar(")")
        self.digit_p = ParseDigit()
        self.solve_p = ParseKeyword("Solve")
        self.st_p = ParseKeyword("such that")

    # 1. Find keyword "Solve"
    # 2. Find all equations...
    # 2.1 Find constants, variables and operators until a comma or a point. If comma, repeat this step.
    # 3. Find keywords "such that"
    # 4. Find constraints...
    # 4.1 Find constants, variables and operators until a comma or a point. If comma, repeat this step.


    equations = []
    constraints = []

    # Helper functions to parse problems to the symbolic classes

    def find_closing_parenthesis(self, string):
        '''
        This helper function returns the position of the closing parenthesis
        '''
        l_parenthesis = 1
        r_parenthesis = 0
        position = 0

        for c in string:
            if c == '(': l_parenthesis += 1
            if c == ')': r_parenthesis += 1

            if l_parenthesis == r_parenthesis:
                return position

            position += 1

    def parse_var_cons(self, string):
        is_constant = False
        is_negative = False
        rest_string = string

        if rest_string[0] == '-':
            is_negative = True
            rest_string = rest_string[1:]
    
        if self.digit_p.parse(rest_string) != []:
            is_constant = True
            full_integer = result(self.digit_p.parse(rest_string))
            rest_string = rest(self.digit_p.parse(rest_string))
            # loop to get full integer
            while self.digit_p.parse(rest_string) != []:
                full_integer = full_integer + result(self.digit_p.parse(rest_string))
                rest_string = rest(self.digit_p.parse(rest_string))

            if is_negative: constant_value =  0 - int(full_integer)
            else: constant_value = int(full_integer)
            result = Constant(constant_value)
        else:
            if is_negative: name = '-' + string[0]
            else: name = string[0]
            result = Variable(name)
            rest_string = string[1:]

        return [(result, rest_string)]



    def parse_operation(self, string):
        '''
        Helper function which parses binary operator and returns the appropriate class and the rest of the string
        '''
        rest_position = 0
        operator_found = False

        while not operator_found:
            if len(string) < rest_position:
                raise RuntimeError(f'Something went wrong parsing an operator in {string}')

            rest_string = string[rest_position:]
            # multiplication: positive integer, opening parenthesis or '*' symbol
            # In first two cases operates "as if the symbol were invisible" and returns the same string as rest
            if self.lp_p.parse(rest_string) != []:
                return [(Multiplication(), rest_string)]
            elif self.digit_p.parse(rest_string) != []:
                return [(Multiplication(), rest_string)]
            # Last case, symbol is explicit therefore the actual rest is returned
            elif rest_string[0] == '*':
                return [(Multiplication(), rest_string[1:])]
            
            # addition: '-' or '+' symbol
            # first case returns the whole string as rest
            elif rest_string[0] == '-':
                return [(Addition(), rest_string)]
            elif rest_string[0] == '+':
                return [('Addition()', rest_string[1:])]

            elif rest_string[0] == ' ':
                rest_position += 1
            # If it's none from the above, then there is no further operator
            else:
                return []
            

    def parse_expression(self, string, arg1=None, arg2=None, operator=None):
        '''
        parse_expression(string, stop_symbol) -> (Expression, rest)
        '''
        # Skip white spaces
        if self.ws_p.parse(string) != []:
            return self.parse_expression(rest(self.ws_p.parse(string)))

        # If there is a parenthesis, apply recursively
        if self.lp_p.parse(string) != []:
            closing_parenthesis = self.find_closing_parenthesis(string)
            # parse next operator
            operator_parser = self.parse_operation(string[closing_parenthesis:])

            if operator_parser != []:
                return self.parse_expression(string[1:closing_parenthesis])
            
            operator = result(operator_parser)

            operator.left_expression = self.parse_expression(string[1:closing_parenthesis])
            operator.right_expression = self.parse_expression(string[closing_parenthesis + 1:])
            return operator
        
        elif arg1 == None:  
            # Expressions should start with constants or variables (after dealing with parenthesis and white spaces)
            term = result(self.parse_var_cons(string))
            rest_string = rest(self.parse_var_cons(string))

            operator_parser = self.parse_operation(rest_string)
            operator = result(operator_parser)
            rest_string = rest(operator_parser)

            return self.parse_expression(rest_string, term, None, operator)

        elif arg2==None:
            if isinstance(operator, Addition):
                operator.left_expression = arg1
                # simpler case:
                # If we already have an arg1 and the operator is "+", no matter what comes next, it will be arg2 as or
                # is the operator with highest precedence.
                term = result(self.parse_var_cons(string))
                rest_string = rest(self.parse_var_cons(string))

                operator_parser = self.parse_operation(rest_string)
                if operator_parser != []:
                    operator.right_expression = term
                else:
                    next_operator = result(operator_parser)
                    rest_string = rest(operator_parser)
                    operator.right_expression = self.parse_expression(rest_string, term, None, next_operator)

                return operator
            elif isinstance(operator, Multiplication):
                """
                Behavior description:
                If we already have an arg1 and the operator is "*", if there is no further operator, arg2 is the next var/const.
                If the next operator is "+", arg1 will store the current "Multiplication" expression and the current operator becomes "+"
                If the next operator is another "*", arg1 will store the current "Multiplication" expression and the current operator becomes "*".
                """
                term = result(self.parse_var_cons(string))
                rest_string = rest(self.parse_var_cons(string))

                operator_parser = self.parse_operation(rest_string)
                if operator_parser != []:
                    next_operator = result(operator_parser)
                    rest_string = rest(operator_parser)

                    operator.left_expression = arg1
                    operator.right_expression = term
                    
                    if isinstance(next_operator, Addition):
                        return self.parse_expression(rest_string, operator, None, next_operator)
                    elif isinstance(next_operator, Multiplication)
                    # Seguir aca, ver comment de la funcion
                else:
                    operator.left_expression = arg1
                    operator.right_expression = term
                
                
            
            
        
    # main parsing function

    def parse_problem(self, current_string, kw1_found=False, kw2_found=False):

        if len(current_string) < 1: return ""

        # White spaces should always be ignored
        elif self.ws_p.parse(current_string) != []:
            rest_string = rest(self.ws_p.parse(current_string))
            return self.parse_problem(rest_string, kw1_found, kw2_found)
        
        # Checks for "Solve"
        elif self.solve_p.parse(current_string) != []:
            rest_string = rest(self.solve_p.parse(current_string))
            return self.parse_problem(rest_string, True, kw2_found)
        
        # Checks for "such that"
        elif self.st_p.parse(current_string) != []:
            rest_string = rest(self.st_p.parse(current_string))
            return self.parse_problem(rest_string, kw1_found, True)
        
        # If kw1 and !kw2, look for equations
        if (kw1_found and not kw2_found):
            equation = Equation()
            # look for an `=` for left_expression
            # parse_equation

        # If kw1 and kw2, look for constraints
