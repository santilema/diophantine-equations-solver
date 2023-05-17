class Equation:
    def __init__(self, left_expression, right_expression):
        self.left_expression = left_expression
        self.right_expression = right_expression

class Expression:
    pass

class Variable(Expression):
    def __init__(self, name):
        self.name = name

class Constant(Expression):
    def __init__(self, value):
        self.value = value

class BinaryOperation(Expression):
    def __init__(self, left_expression, right_expression):
        self.left_expression = left_expression
        self.right_expression = right_expression

class Addition(BinaryOperation):
    pass

class Subtraction(BinaryOperation):
    pass

class Multiplication(BinaryOperation):
    pass
