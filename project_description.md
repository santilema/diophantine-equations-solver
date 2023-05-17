# Joint paper

## BNF Grammar

```bnf
<task> ::= 'Solve' <system>
<system> ::= <equality> '.' | <equality> ',' <system> | <equality> 'such that' <constraint>
<constraint> ::= <boolean> '.' | <boolean> ',' <constraint> '.'
<boolean> ::= <inequality> | <boolean> <bool_operator> <boolean>
<bool_operator> ::= 'and' | 'or'
<equality> ::= <arithmetic_expr> '=' <arithmetic_expr>
<inequality> ::= <arithmetic_expr> <inequality_operator> <arithmetic_expr>
<inequality_operator> ::= '>' | '<'
<arithmetic_expr> ::= <integer> | <variable> | <arithmetic_expr> <arithmetic_operator> <arithmetic_expr>
<arithmetic_operator> ::= '+' | '-' | '*'
<integer> ::= <digit> | <digit> <integer>
<variable> ::= [a-z]
<digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9

```
