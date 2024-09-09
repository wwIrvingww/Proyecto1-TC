from ShuntingYard import shunting_yard
from thompson import get_alphabet, thomspon_main
from subset import set_main
from Hopcroft import cross_product_accept_not_accept, find_transition_pairs, cross_product_states, generate_reduced_automaton, difference_between_lists
from simulacion import simulate_afd
import json

r = input("Ingresa la expresión regular: ")
w = input("Ingresa la cadena a validar: ")


print("\n***")
# Convierte a postfix
postfix = shunting_yard(r)
print("*** \n")

# convierte a no determinista
afn = thomspon_main(postfix)
# convierte a determinista
afd = set_main(afn)

initial_cross_product = cross_product_accept_not_accept(afd)
final_pairs = find_transition_pairs(afd, initial_cross_product)
states_product = cross_product_states(afd)
difference = difference_between_lists(states_product, final_pairs)
new_automaton = generate_reduced_automaton(afd, difference)

print("***")
# por ahora, lo guarda en el finite_deterministic.json
if afd:
    print("AFD:\n", afd)
    
    with open('finite_deterministic.json', 'w') as json_file:
        json.dump(afd, json_file, indent=4)
        print("El nuevo autómata ha sido exportado a 'finite_deterministic.json'.")
print("*** \n")

print("***")
if new_automaton:
    print("New Automaton:\n", new_automaton)
    
    # Exportar el autómata a un archivo JSON
    with open('reduced_automaton.json', 'w') as json_file:
        json.dump(new_automaton, json_file, indent=4)
        print("El nuevo autómata ha sido exportado a 'reduced_automaton.json'.")
print("*** \n")


print("***")
simulate_afd(afd, w)
print("*** \n")

