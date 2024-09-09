def simulate_afd(afd, w):
    # Estado inicial
    estado_actual = afd["q0"]
    
    # Procesar cada símbolo de la cadena de entrada
    for simbolo in w:
        # Crear la clave de transición (estado_actual, simbolo)
        transicion = f"({estado_actual},{simbolo})"
        
        # Verificar si existe una transición para el estado actual y el símbolo
        if transicion in afd["δ"]:
            # Moverse al siguiente estado
            estado_actual = afd["δ"][transicion]
        else:
            # No hay transición válida, la cadena no es aceptada
            print(f"No hay transición para el estado {estado_actual} con el símbolo {simbolo}.")
            return False
    
    # Verificar si el estado actual es un estado de aceptación
    if estado_actual in afd["F"]:
        print(f"La cadena '{w}' es aceptada por el autómata.")
        return True
    else:
        print(f"La cadena '{w}' no es aceptada por el autómata.")
        return False
    