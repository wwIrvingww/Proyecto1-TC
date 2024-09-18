from ShuntingYard import shunting_yard
from thompson import get_alphabet, thomspon_main
from subset import set_main
from Hopcroft import hopcroft_minimization
from simulacion import simulate_afd, simulate_afn
import json
import graph

# Paso 1. Se obtiene la regexp en infix y la cadena a validar
r = input("Ingresa la expresión regular: ")
w = input("Ingresa la cadena a validar: ")
print("\n***")

# Paso 2. Convierte a postfix
postfix = shunting_yard(r)
print("*** \n")

# Paso 3. Convierte a automata no determinista en forma json
afn = thomspon_main(postfix)

# Paso 4. Convierte a automata determinista
afd = set_main(afn)

# Paso 5. Minimiza el afd utilizando el algoritmo de Hopcroft
new_automaton = hopcroft_minimization(afd)

# Paso 6. Impresión de resultado
print("***")
# 6.1 afn
if afn:
    print("AFN:\n", afn) # Se imprime
    with open('./automatas/finite_non_deterministic.json', 'w') as json_file: # Se guarda en JSON
        json.dump(afn, json_file, indent=4)
        print("El autómata finito no determinista ha sido exportado a 'finite_non_deterministic.json'.")
print("*** \n")
print("***")

# 6.2 afd no reducido
if afd:
    print("AFD:\n", afd) # Se imprime
    with open('./automatas/deterministic_automaton.json', 'w') as json_file: # Se guarda en JSON
        json.dump(afd, json_file, indent=4)
    print("El nuevo autómata ha sido exportado a 'deterministic_automaton.json'.")
print("*** \n")
print("***")

# 6.3 afd reducido
if afd:
    print("Reduced:\n", new_automaton) # Se imprime
    with open('./automatas/reduced_automaton.json', 'w') as json_file: # Se guarda en JSON
        json.dump(new_automaton, json_file, indent=4)
    print("El nuevo autómata ha sido exportado a 'reduced_automaton.json'.")
print("*** \n")

# Paso 7. Simulación de los autómatas

# 7.1 simulación AFD
print("*** \nAFD")
resultado_afd = simulate_afd(afd, w)
print(f"Resultado: {resultado_afd['resultado']}")
print(f"Tiempo de ejecución: {resultado_afd['tiempo']} segundos")
print("Transiciones realizadas:")
for transicion in resultado_afd["transiciones"]:
    print(f"{transicion[0]} --({transicion[1]})--> {transicion[2]}")
print("*** \n")

# 7.2 simulación AFD reducido
print("*** \nAFD REDUCIDO")
resultado_red = simulate_afd(new_automaton, w)
print(f"Resultado: {resultado_red['resultado']}")
print(f"Tiempo de ejecución: {resultado_red['tiempo']} segundos")
print("Transiciones realizadas:")
for transicion in resultado_red["transiciones"]:
    print(f"{transicion[0]} --({transicion[1]})--> {transicion[2]}")
print("*** \n")

# 7.3 Simulación AFN
print("*** \nAFN")
simulate_afn(afn, w)
print("*** \n")

# Paso 8. Estructura de grafo dirigido
graph.graph_main(new_automaton)
