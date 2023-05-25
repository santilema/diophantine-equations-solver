def solve(description_path):
    """
    >>> sol = solve('examples/example5.txt')
    >>> sol
    {'z': 0, 'u': 7, 'v': -1, 'x': 1, 'y': -3, 't': 7}
    """
    file = open(description_path).read()
    print(file)

solve("examples/example5.txt")
