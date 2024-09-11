def add_concatenation_operator(expression):
    new_expression = []
    for i, token in enumerate(expression):
        new_expression.append(token)
        
        # Verifica si es necesario agregar el operador de concatenación.
        if i < len(expression) - 1:
            current = expression[i]
            next_token = expression[i + 1]
            
            # Si el actual es un alfanumérico o cierre de paréntesis
            # y el siguiente es un alfanumérico o apertura de paréntesis
            if (current.isalnum() or current == '*' or current == ')' or current == '%') and (next_token.isalnum() or next_token == '(' or next_token == '%'):
                new_expression.append('.')
    
    return ''.join(new_expression)

def shunting_yard(expression):
    # Define la precedencia de los operadores
    precedence = {'*': 3, '.': 2, '|': 1, '(': 0}
    operators = []
    output = []
    
    # Modifica la expresión para agregar el operador de concatenación implícito
    expression = add_concatenation_operator(expression)
    
    for token in expression:
        if token.isalnum() or token == '%':  # Si el token es un símbolo del alfabeto o epsilon 
            output.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()  # Quita el '(' de la pila
        elif token == '*':
            # El operador de Kleene siempre se aplica inmediatamente, sin pop
            output.append(token)
        else:
            while (operators and precedence[operators[-1]] >= precedence[token]):
                output.append(operators.pop())
            operators.append(token)
    
    while operators:
        output.append(operators.pop())
        
    print("Postfix: ", ''.join(output))
    
    return ''.join(output)