from z3 import *

class Equation:
    def __init__(self, left_expression, right_expression):
        self.left_expression = left_expression
        self.right_expression = right_expression

    def __str__(self):
        return f"{self.left_expression} = {self.right_expression}"
    
    def toz3(self):
        return self.left_expression.toz3() == self.right_expression.toz3()

class Expression:
    def __add__(self, other):
        return Addition(self, other)
    
    def __mul__(self, other):
        return Multiplication(self, other)

class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Variable({self.name})"
    
    def toz3(self):
        return Int(self.name)
    
    def evaluate(self, variable_values):
        return variable_values[self.name]

class Constant(Expression):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return f"Constant({self.value})"
    
    def evaluate(self, variable_values):
        return self.value
    
    def toz3(self):
        return self.value

class BinaryOperation(Expression):
    def __init__(self, left_expression, right_expression):
        self.left_expression = left_expression
        self.right_expression = right_expression

class Addition(BinaryOperation):
    def __init__(self, left_expression=None, right_expression=None):
        super().__init__(left_expression, right_expression)
    
    def __str__(self):
        return f"({self.left_expression} + {self.right_expression})"
    
    def __repr__(self):
        return f"Addition({self.left_expression}, {self.right_expression})"
    
    def toz3(self):
        return Sum(self.left_expression.toz3(), self.right_expression.toz3())
    
    def evaluate(self, variable_values):
        return self.left_expression.evaluate(variable_values) + self.right_expression.evaluate(variable_values)

class Multiplication(BinaryOperation):
    def __init__(self, left_expression=None, right_expression=None):
        super().__init__(left_expression, right_expression)

    def __str__(self):
        return f"({self.left_expression} * {self.right_expression})"
    
    def __repr__(self):
        return f"Multiplication({self.left_expression}, {self.right_expression})"
    
    def toz3(self):
        return Product(self.left_expression.toz3(), self.right_expression.toz3())

    def evaluate(self, variable_values):
        return self.left_expression.evaluate(variable_values) * self.right_expression.evaluate(variable_values)

class Conjunction(BinaryOperation):
    def __init__(self, left_expression=None, right_expression=None):
        super().__init__(left_expression, right_expression)

    def __str__(self):
        return f"({self.left_expression} and {self.right_expression})"
    
    def __repr__(self):
        return f"Conjunction({self.left_expression}, {self.right_expression})"
    
    def toz3(self):
        return And(self.left_expression.toz3(), self.right_expression.toz3())

    def evaluate(self, variable_values):
        return self.left_expression.evaluate(variable_values) and self.right_expression.evaluate(variable_values)
    
class OrUnion(BinaryOperation):
    def __init__(self, left_expression=None, right_expression=None):
        super().__init__(left_expression, right_expression)

    def __str__(self):
        return f"({self.left_expression} or {self.right_expression})"
    
    def __repr__(self):
        return f"Union({self.left_expression}, {self.right_expression})"
    
    def toz3(self):
        return Or(self.left_expression.toz3(), self.right_expression.toz3())

    def evaluate(self, variable_values):
        return self.left_expression.evaluate(variable_values) or self.right_expression.evaluate(variable_values)
    
class GreaterThan(BinaryOperation):
    def __init__(self, left_expression=None, right_expression=None):
        super().__init__(left_expression, right_expression)

    def __str__(self):
        return f"({self.left_expression} > {self.right_expression})"
    
    def __repr__(self):
        return f"GreaterThan({self.left_expression}, {self.right_expression})"
    
    def toz3(self):
        return self.left_expression.toz3() > self.right_expression.toz3()

    def evaluate(self, variable_values):
        return self.left_expression.evaluate(variable_values) > self.right_expression.evaluate(variable_values)
    
class LessThan(BinaryOperation):
    def __init__(self, left_expression=None, right_expression=None):
        super().__init__(left_expression, right_expression)

    def __str__(self):
        return f"({self.left_expression} < {self.right_expression})"
    
    def __repr__(self):
        return f"LessThan({self.left_expression}, {self.right_expression})"
    
    def toz3(self):
        return self.left_expression.toz3() < self.right_expression.toz3()

    def evaluate(self, variable_values):
        return self.left_expression.evaluate(variable_values) < self.right_expression.evaluate(variable_values)

#############################################
