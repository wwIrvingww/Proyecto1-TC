from ShuntingYard import shunting_yard
from thompson import get_alphabet, thomspon_main
from subset import set_main
from Hopcroft import hopcroft_minimization
from simulacion import simulate_afd, simulate_afn
import json

r = input("Ingresa la expresión regular: ")
w = input("Ingresa la cadena a validar: ")

print("\n***")
# Convierte a postfix
postfix = shunting_yard(r)
print("*** \n")

# Convierte a no determinista
afn = thomspon_main(postfix)

# Convierte a determinista
afd = set_main(afn)

# Utiliza el algoritmo de Hopcroft para minimizar el AFD
new_automaton = hopcroft_minimization(afd)

print("***")
# Guarda el AFN en un archivo JSON
if afn:
    print("AFN:\n", afn)
    with open('finite_non_deterministic.json', 'w') as json_file:
        json.dump(afn, json_file, indent=4)
        print("El autómata finito no determinista ha sido exportado a 'finite_non_deterministic.json'.")
print("*** \n")

print("***")
# Guarda el AFD en un archivo JSON
if afd:
    print("AFD:\n", afd)
    # Guardar el autómata minimizado en un archivo JSON
    with open('deterministic_automaton.json', 'w') as json_file:
        json.dump(afd, json_file, indent=4)
    print("El nuevo autómata ha sido exportado a 'deterministic_automaton.json'.")
print("*** \n")

print("***")
# Guarda el AFD en un archivo JSON
if afd:
    print("Reduced:\n", new_automaton)
    # Guardar el autómata minimizado en un archivo JSON
    with open('reduced_automaton.json', 'w') as json_file:
        json.dump(new_automaton, json_file, indent=4)
    print("El nuevo autómata ha sido exportado a 'reduced_automaton.json'.")
print("*** \n")

# Simulación del AFD original
print("*** \nAFD")
resultado_afd = simulate_afd(afd, w)
print(f"Resultado: {resultado_afd['resultado']}")
print(f"Tiempo de ejecución: {resultado_afd['tiempo']} segundos")
print("Transiciones realizadas:")
for transicion in resultado_afd["transiciones"]:
    print(f"{transicion[0]} --({transicion[1]})--> {transicion[2]}")
print("*** \n")

# Simulación del AFD reducido
print("*** \nAFD REDUCIDO")
resultado_red = simulate_afd(new_automaton, w)
print(f"Resultado: {resultado_red['resultado']}")
print(f"Tiempo de ejecución: {resultado_red['tiempo']} segundos")
print("Transiciones realizadas:")
for transicion in resultado_red["transiciones"]:
    print(f"{transicion[0]} --({transicion[1]})--> {transicion[2]}")
print("*** \n")

# Simulación del AFN
print("*** \nAFN")
simulate_afn(afn, w)
print("*** \n")
