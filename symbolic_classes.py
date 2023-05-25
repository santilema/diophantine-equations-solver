from z3 import *

class Equation:
    def __init__(self, left_expression, right_expression):
        self.left_expression = left_expression
        self.right_expression = right_expression

class Expression:
    def __add__(self, other):
        return Addition(self, other)
    
    def __sub__(self, other):
        return Subtraction(self, other)
    
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
    def __init__(self, left_expression, right_expression):
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
    def __init__(self, left_expression, right_expression):
        super().__init__(left_expression, right_expression)

    def __str__(self):
        return f"({self.left_expression} * {self.right_expression})"
    
    def __repr__(self):
        return f"Multiplication({self.left_expression}, {self.right_expression})"
    
    def toz3(self):
        return Product(self.left_expression.toz3(), self.right_expression.toz3())

    def evaluate(self, variable_values):
        return self.left_expression.evaluate(variable_values) * self.right_expression.evaluate(variable_values)


#############################################

# Some examples of how to use the classes above

# 1. Create a variable
x = Variable("x")
print(x) # x

# 2. Create a constant
c = Constant(5)
print(c) # 5

# 3. Create an expression
e = x + c
print(e) # (x + 5)

# 4. Evaluate an expression
variable_values = {"x": 10}
print(e.evaluate(variable_values)) # 15

# 5. Create z3 sum
sum_z3 = e.toz3()
print(sum_z3)
