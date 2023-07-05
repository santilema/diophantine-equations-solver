# Description of the work

## Parsing

The basic-level parsers were taken from the code studied during the lectures. With those, more complex parsers were built. Starting with a *Keyword Parser* which simplified the task of spotting the keywords which divided the equations from the constraints, and was also useful to skip new-line break by spotting the backslash and the letter n as a keyword.

A single class was created for parsing the entire system description which depends on many parsing functions. There are functions to parse equations, expressions, operators and constants or variables. They all make use of simpler parsers such as the *Keyword, Character* and *Digit* parsers.

Also some other helper methods were implemented to accomplish the task of parsing equations. There is, for example, a method *search_in_same_level* which takes a parser attribute which will be applied only in the current level of the equation skipping everything between parenthesis.

### String-formatter

There is an extra file to the project with a pre-processing function. The need for this came from a difficulty to deal with all possible notations for multiplication strings. The string-formatter will transform any of this notations to: `arg1 * arg2` before even starting the previously described parsing process.

## Symbolic classes

The symbolic classes, inspired on the BNF grammar and the code discussed in the lectures as well, comprehend equations, binary operations (multiplication, and, greater than, etc.), variables and constants. All of them with self-introductory names except of *OrUnion* which corresponds to an `or` operator but the name was taken by the Z3 class, and *Union* already existed in Python as well. Just in case, the weird name was chosen.

### Z3_methods

All classes have a *toz3* method. The higher level classes will call the same method of lower level ones, allowing the instantiation of their z3-equivalent classes.

## Potential extension

As for potential extensions, it could be useful to have an extra attribute to retrieve more than just one solution model if it exists.
