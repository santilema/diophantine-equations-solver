from z3 import *
from parsers import *

def solve(description_path):
    """
    Solves a diophantine equation problem given a path to a file containing the problem description. Examples:
    >>> solve("examples/example1.txt")
    [z = -11, y = 27, x = -6]
    >>> solve("examples/example2.txt")
    [y = 3, z = 0, x = 0, u = 0]
    >>> solve("examples/example3.txt")
    [x = 3, z = -1, y = -18]
    >>> solve("examples/example4.txt")
    No solution!
    >>> solve("examples/example5.txt")
    [t = 6, v = -5, u = 7, z = -8, x = 1, y = -2]
    """
    file = open(description_path).read()

    # parse expression and instantiate classes
    parser = ParseDiophantine()
    parsed = parser.parse_problem(file)

    equations = []
    constraints = []
    for eq in parsed['equations']:
        equations.append(eq.toz3())
    for con in parsed['constraints']:
        constraints.append(con.toz3())

    # solve classes using toz3() methods
    solver = Solver()
    solver.add(equations)
    solver.add(constraints)

    # check if problem is solvable
    if solver.check() == sat:
        model = solver.model()
        print(model)
    else:
        print("No solution!")
