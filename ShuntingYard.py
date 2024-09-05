def shunting_yard(expression):
    precedence = {'*': 3, '.': 2, '|': 1, '(': 0}
    operators = []
    output = []
    
    for token in expression:
        if token.isalnum():  # Si el token es un símbolo del alfabeto
            output.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()  # Quita el '(' de la pila
        else:
            while (operators and precedence[operators[-1]] >= precedence[token]):
                output.append(operators.pop())
            operators.append(token)
    
    while operators:
        output.append(operators.pop())
    
    return ''.join(output)
