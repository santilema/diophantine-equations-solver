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
        self.white_space_parser = ParseChar(" ")
        self.l_parenthesis_parser = ParseChar("(")
        self.r_parenthesis_parser = ParseChar(")")
        self.digit_parser = ParseDigit()
        self.solve_parser = ParseKeyword("Solve")
        self.such_that_parser = ParseKeyword("such that")

    # 1. Find keyword "Solve"
    # 2. Find all equations...
    # 2.1 Find constants, variables and operators until a comma or a point. If comma, repeat this step.
    # 3. Find keywords "such that"
    # 4. Find constraints...
    # 4.1 Find constants, variables and operators until a comma or a point. If comma, repeat this step.

    equations = []
    constraints = []