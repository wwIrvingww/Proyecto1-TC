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


