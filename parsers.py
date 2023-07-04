from symbolic_classes import *
from string_formater import *

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
        
class ParseDiophantine():
    def __init__(self):
        self.ws_p = ParseChar(" ")
        self.lp_p = ParseChar("(")
        self.rp_p = ParseChar(")")
        self.comma_p = ParseChar(",")
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
            term = Constant(constant_value)
        else:
            if is_negative: name = '-' + string[0]
            else: name = string[0]
            term = Variable(name)
            rest_string = string[1:]

        return [(term, rest_string)]



    def parse_operation(self, string, addition=True, multiplication=True):
        '''
        Helper function which parses binary operator and returns the appropriate class and the rest of the string
        '''
        rest_position = 0
        rest_string = string

        while len(rest_string) > 1:
            rest_string = string[rest_position:]

            # if there is a parenthesis, return the closing parenthesis position and the next operator (if any)
            # This intends to just return operators in the current level of the parsing tree
            if self.lp_p.parse(rest_string) != []:
                closing_parenthesis_finder = self.find_closing_parenthesis(string[rest_position:])
                closing_parenthesis = closing_parenthesis_finder["closing_parenthesis"]
                next_operator = closing_parenthesis_finder["next_operator"]
                if next_operator != []:
                    return [(result(next_operator), string[closing_parenthesis + 1:]), closing_parenthesis + 1]
                else:
                    return []
        
            if (multiplication):
                # multiplication: positive integer, opening parenthesis or '*' symbol
                # In first two cases operates "as if the symbol were invisible" and returns the same string as rest
                if rest_string[0] == '*':
                    return [(Multiplication(), rest_string[1:]), rest_position + 1]
            
            if (addition):
                # addition: '-' or '+' symbol
                # first case returns the whole string as rest
                if rest_string[0] == '-':
                    return [(Addition(), rest_string), rest_position + 1]
                elif rest_string[0] == '+':
                    return [(Addition(), rest_string[1:]), rest_position + 1]

            rest_position += 1
        # If it's none from the above, then there is no further operator
        return []
            
    def find_closing_parenthesis(self, string):
        '''
        This helper function returns the position of the closing parenthesis
        and the next operator (if any)
        '''
        l_parenthesis = 0
        r_parenthesis = 0
        position = 0

        for c in string:
            if c == '(': l_parenthesis += 1
            if c == ')': r_parenthesis += 1

            if l_parenthesis == r_parenthesis:
                # evaluate position is not the last character
                if position < len(string) - 1:
                    # if the next character is an operator, return it
                    if self.parse_operation(string[position + 1:]) != []:
                        return {
                            "closing_parenthesis": position,
                            "next_operator": self.parse_operation(string[position + 1:])
                        } 
                return {
                    "closing_parenthesis": position,
                    "next_operator": []
                }
            position += 1
            

    def parse_expression(self, string):
        '''
        parse_expression(string, stop_symbol) -> (Expression, rest)
        '''

        # If there is a parenthesis, apply recursively
        if self.lp_p.parse(string) != []:
            closing_parenthesis_finder = self.find_closing_parenthesis(string)
            closing_parenthesis = closing_parenthesis_finder["closing_parenthesis"]
            next_operator = closing_parenthesis_finder["next_operator"]

            # if there is no further operator, return the expression inside the parenthesis
            if next_operator == []:
                return self.parse_expression(string[1:closing_parenthesis])
            else:
                next_operator = result(next_operator)
                # The operator is a class already
                next_operator.left_expression = self.parse_expression(string[1:closing_parenthesis])
                next_operator.right_expression = self.parse_expression(string[closing_parenthesis + 1:])
            

            operator.left_expression = self.parse_expression(string[1:closing_parenthesis])
            
            # If operator is Addition, parse the right expression
            if isinstance(operator, Addition):
                operator.right_expression = self.parse_expression(string[closing_parenthesis + 1:])
                return operator
            # If operator is Multiplication, look for an operator with higher precedence
            elif isinstance(operator, Multiplication):
                next_addition = self.parse_operation(string[closing_parenthesis + 1:], multiplication=False)
                # If there is no further sum operator, return the expression inside the parenthesis
                if next_addition == []:
                    operator.right_expression = self.parse_expression(string[closing_parenthesis + 1:])
                    return operator
                # If there is a further operator and it is Addition, return the addition with the multiplication as left expression
                else:
                    if isinstance(result(next_addition), Addition):
                        expression_end = next_addition[1]
                        next_addition = result(next_addition)
                        operator.right_expression = self.parse_expression(string[closing_parenthesis + 1:expression_end])
                        next_addition.left_expression = operator
                        next_addition.right_expression = self.parse_expression(string[expression_end + 1:])
                        return next_addition
        else:
            # Expressions should start with constants or variables (after dealing with parenthesis and white spaces)
            term = result(self.parse_var_cons(string))
            rest_string = rest(self.parse_var_cons(string))

            operator_parser = self.parse_operation(rest_string)

            # If there is no operator, return the term
            if operator_parser == []:
                return term
            else:
                operator = result(operator_parser)
                rest_string = rest(operator_parser)
                # If the operator is an Addition, parse the right expression
                if isinstance(operator, Addition):
                    operator.left_expression = term
                    operator.right_expression = self.parse_expression(rest_string)
                    return operator
                # If the operator is a Multiplication, look for an operator with higher precedence
                elif isinstance(operator, Multiplication):
                    next_addition = self.parse_operation(rest_string, multiplication=False)
                    # If there is no further sum operator, parse the right expression and return the multiplication
                    if next_addition == []:
                        operator.left_expression = term
                        operator.right_expression = self.parse_expression(rest_string)
                        return operator
                    # If there is a further operator and it is Addition, return the addition with the multiplication as left expression
                    else:
                        expression_end = next_addition[1]
                        next_addition = result(next_addition)
                        operator.left_expression = term
                        operator.right_expression = self.parse_expression(rest_string[:expression_end])
                        next_addition.left_expression = operator
                        next_addition.right_expression = self.parse_expression(rest_string[expression_end + 1:])
                        return next_addition
                    
    def parse_equation(self, string):
        # Position of the equal sign
        equal_position = string.find('=')
        left_expression = self.parse_expression(format_string(string[:equal_position]))
        right_expression = self.parse_expression(format_string(string[equal_position + 1:]))
        return Equation(left_expression, right_expression)
                
    def equations_finder(self, string):
        position = 0
        current_equation = ''
        found_equations = []
        while position < len(string):
            current_character = string[position]
            if self.ws_p.parse(string[position:]) != []:
                position += 1
                continue # skip white spaces
            elif self.st_p.parse(string[position:]) != []:
                # found keyword "such that", return the equations and the rest of the string
                found_equations.append(current_equation)
                return {
                    "found_expressions": found_equations,
                    "rest_string": string[position + 1:]
                }
            elif self.comma_p.parse(string[position:]) != []:
                # found comma, add the equation to the list and reset the current equation
                found_equations.append(current_equation)
                current_equation = ''
            else:
                current_equation += current_character
            position += 1
        # if the end of the string is reached, return the equations and the rest of the string
        found_equations.append(current_equation)
        return {
            "found_expressions": found_equations,
            "rest_string": ""
        }
            
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
        
        # If kw1 and !kw2, look for equations
        if (kw1_found and not kw2_found):
            # Find all equations
            equation_finder = self.equations_finder(current_string)
            equations = equation_finder["found_expressions"]
            rest_string = equation_finder["rest_string"]

            # Parse equations to symbolic classes
            symbolic_equations = []
            for equation in equations:
                symbolic_equations.append(self.parse_equation(equation))

            return {
                "equations": symbolic_equations,
                "constraints": self.parse_problem(rest_string, kw1_found, True)
            }

        # If kw1 and kw2, look for constraints
        elif (kw1_found and kw2_found):
            if len(current_string) < 1: return ""


# Testing the parser

# without constraints
# problem0 = " Solve  x + 2 = 3"
# problem1 = " Solve  x + 2 = 3, y + 3 = 4"
# problem2 = " Solve  x + 2 = 3, y + 3 = 4, x*2 = 4"
# problem3 = " Solve x + 2 = 3, y + 3 = 4, x*2 = 4, y * (2 + y) = 6"
# problem4 = " Solve y * (2 + y) + 1 = y * (2 + x), x = 2"

# parser = ParseDiophantine()

# for equation in parser.parse_problem(problem4)["equations"]:
#     print(equation)