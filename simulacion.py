import time

def simulate_afd(afd, w):
    # Estado inicial
    estado_actual = afd["q0"]
    transiciones_realizadas = []  
    
    # Medir el tiempo de ejecución
    start_time = time.time()
    
    # Procesar cada símbolo de la cadena de entrada
    for simbolo in w:
        # Crear la clave de transición (estado_actual, simbolo)
        transicion = f"({estado_actual},{simbolo})"
        
        # Verificar si existe una transición para el estado actual y el símbolo
        if transicion in afd["δ"]:
            # Moverse al siguiente estado y registrar la transición
            estado_siguiente = afd["δ"][transicion]
            transiciones_realizadas.append((estado_actual, simbolo, estado_siguiente))
            estado_actual = estado_siguiente
        else:
            # No hay transición válida, la cadena no es aceptada
            print(f"No hay transición para el estado {estado_actual} con el símbolo {simbolo}.")
            end_time = time.time()
            tiempo_ejecucion = end_time - start_time
            return {
                "resultado": "NO",
                "tiempo": f"{tiempo_ejecucion:.8f}",  # Tiempo con 8 decimales
                "transiciones": transiciones_realizadas
            }
    
    # Verificar si el estado actual es un estado de aceptación
    if estado_actual in afd["F"]:
        end_time = time.time()
        tiempo_ejecucion = end_time - start_time
        return {
            "resultado": "SÍ",
            "tiempo": f"{tiempo_ejecucion:.10f}",  
            "transiciones": transiciones_realizadas
        }
    else:
        end_time = time.time()
        tiempo_ejecucion = end_time - start_time
        return {
            "resultado": "NO",
            "tiempo": f"{tiempo_ejecucion:.10f}",  #
            "transiciones": transiciones_realizadas
        }


def epsilon_cerradura(afd, estados):
    cerradura = set(estados)  # Conjunto de estados
    stack = list(estados)   # Pila de estados a procesar

    while stack:
        estado = stack.pop()
        transicion_eps = f"({estado},%)"
        
        if transicion_eps in afd["δ"]:
            for siguiente_estado in afd["δ"][transicion_eps]:
                if siguiente_estado not in cerradura:
                    cerradura.add(siguiente_estado)
                    stack.append(siguiente_estado)

    return cerradura


def simulate_afn(afn, w):
    # Inicializamos con el cierre epsilon del estado inicial
    estados_actuales = epsilon_cerradura(afn, [afn["q0"]])
    transiciones_realizadas = []
    
    # Medir el tiempo de ejecución
    start_time = time.time()
    
    # Procesar cada símbolo de la cadena de entrada
    for simbolo in w:
        nuevos_estados = set()
        
        for estado in estados_actuales:
            # Crear la clave de transición (estado_actual, simbolo)
            transicion = f"({estado},{simbolo})"
            
            if transicion in afn["δ"]:
                for siguiente_estado in afn["δ"][transicion]:
                    nuevos_estados.add(siguiente_estado)
                    transiciones_realizadas.append(f"{estado} --({simbolo})--> {siguiente_estado}")
        
        # Ahora hacemos el cierre epsilon de los nuevos estados
        estados_actuales = epsilon_cerradura(afn, nuevos_estados)
    
    # Verificamos si algún estado actual es de aceptación
    es_aceptado = any(estado in afn["F"] for estado in estados_actuales)
    end_time = time.time()
    tiempo_de_ejecucion  = end_time - start_time

    # Mostrar resultado
    if es_aceptado:
        print(f"Resultado: SÍ \nTiempo:" f"{tiempo_de_ejecucion:.10f}")
    else:
        print(f"Resultado: NO")

    print("Transiciones realizadas:")
    for transicion in transiciones_realizadas:
        print(transicion)

    return es_aceptado

