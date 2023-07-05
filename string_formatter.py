def format_string(input_string):
    transformed_string = ""

    i = 0
    while i < len(input_string):
        current_char = input_string[i]

        # Replace 'c(' with 'c*('
        if (current_char.isalpha() or current_char.isdigit()) and i + 1 < len(input_string) and input_string[i + 1] == '(':
            transformed_string += current_char + '*('
            i += 1

        # Replace ')c' with ')*c'
        elif current_char == ')' and i + 1 < len(input_string) and (input_string[i + 1].isalpha() or input_string[i + 1].isdigit()):
            transformed_string += ')*' + input_string[i + 1]
            i += 1

        # Replace ')(' with ')*('
        elif current_char == ')' and i + 1 < len(input_string) and input_string[i + 1] == '(':
            transformed_string += ')*('

        # Replace 'ln' with 'l*n'
        elif current_char.isalpha() and i + 1 < len(input_string) and input_string[i + 1].isdigit():
            transformed_string += current_char + '*' + input_string[i + 1]
            i += 1

        # Replace 'nl' with 'n*l'
        elif current_char.isdigit() and i + 1 < len(input_string) and input_string[i + 1].isalpha():
            transformed_string += current_char + '*' + input_string[i + 1]
            i += 1

        else:
            transformed_string += current_char

        i += 1

    return transformed_string
