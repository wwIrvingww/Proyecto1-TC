import itertools
import json

def cross_product_accept_not_accept(afn):
    states = afn["Q"]
    accepting_states = afn["F"]
    non_accepting_states = [state for state in states if state not in accepting_states]
    cross_product = list(itertools.product(accepting_states, non_accepting_states))
    return cross_product

def find_transition_pairs(afn, cross_product):
    transitions = afn["δ"]
    alphabet = afn["Σ"]
    
    # Eliminar epsilon del alfabeto si está presente
    if '%' in alphabet:
        alphabet.remove('%')
    
    new_pairs = set(tuple(sorted(pair)) for pair in cross_product)

    while True:
        added_new_pairs = False
        
        current_pairs = list(new_pairs)
        for (q_accept, q_non_accept) in current_pairs:
            for symbol in alphabet:
                q_accept_from_states = []
                q_non_accept_from_states = []
                
                for (key, value) in transitions.items():
                    state, transition_symbol = key.strip("()").split(',')
                    state = state.strip()
                    transition_symbol = transition_symbol.strip()

                    if transition_symbol == symbol:
                        if value == q_accept:
                            q_accept_from_states.append(state)
                        if value == q_non_accept:
                            q_non_accept_from_states.append(state)
                
                # Generar todas las combinaciones posibles de estados anteriores con el mismo símbolo
                for q_accept_from in q_accept_from_states:
                    for q_non_accept_from in q_non_accept_from_states:
                        new_pair = tuple(sorted((q_accept_from, q_non_accept_from)))
                        if new_pair not in new_pairs:
                            new_pairs.add(new_pair)
                            added_new_pairs = True
                            print(f"Added new pair: {new_pair} via symbol: {symbol}")

        if not added_new_pairs:
            break

    return list(new_pairs)

# Cross product with states
def cross_product_states(afn):
    states = afn["Q"]
    cross_product = []

    # Generar el producto cruzado excluyendo pares de estados idénticos y eliminando duplicados
    for state1, state2 in itertools.combinations(states, 2):
        cross_product.append((state1, state2))
    
    return cross_product

def difference_between_lists(A, B, estado_inicial):
    # Convertir cada par en un conjunto ordenado para ignorar el orden
    set_A = {tuple(sorted(pair)) for pair in A}
    set_B = {tuple(sorted(pair)) for pair in B}

    # Calcular la diferencia
    difference = set_A - set_B

    # Asegurarse de que el estado inicial esté en la diferencia
    for pair in set_A:
        if estado_inicial in pair:
            difference.add(pair)
    
    # Convertir de nuevo a una lista de tuplas
    return list(difference)



# Generate the reduced automaton
def generate_reduced_automaton(afn, difference):
    if not difference:
        print("El autómata ya no se puede reducir más.")
        return None

    state_mapping = {}
    new_transitions = {}
    new_initial_state = None
    new_accepting_states = set()

    # Generar nuevos estados
    for i, pair in enumerate(difference):
        state_name = chr(65 + i)
        print(f"Mapeando el par {pair} al nuevo estado {state_name}")
        state_mapping[pair] = state_name
        
        # Verificar si alguno de los estados en el par es el estado inicial original
        if afn["q0"] in pair:
            new_initial_state = state_name
            print(f"Estado inicial encontrado: {new_initial_state}")
        
        # Asignar estados finales
        if any(state in afn["F"] for state in pair):
            new_accepting_states.add(state_name)

    # Asegurarse de que el estado inicial no sea None
    if new_initial_state is None:
        print("Error: No se ha encontrado un estado inicial.")
        return None

    # Mapear transiciones
    for pair, new_state in state_mapping.items():
        for state in pair:
            for symbol in afn["Σ"]:
                transition_key = f"({state},{symbol})"
                if transition_key in afn["δ"]:
                    target_state = afn["δ"][transition_key]
                    for target_pair, target_new_state in state_mapping.items():
                        if target_state in target_pair:
                            new_transition_key = f"({new_state},{symbol})"
                            new_transitions[new_transition_key] = target_new_state
                            print(f"Mapeando transición {transition_key} -> {new_transition_key}")

    # Construir el nuevo autómata
    new_automaton = {
        "Q": list(state_mapping.values()),
        "Σ": afn["Σ"],
        "q0": new_initial_state,  # Estado inicial correcto
        "F": list(new_accepting_states),
        "δ": new_transitions
    }

    print("Nuevo autómata generado correctamente.")
    return new_automaton




# Ejemplo de uso con el AFN proporcionado
afn_example = {
    "Q": ["q0", "q1", "q2", "q3"],
    "Σ": ["0", "1"],
    "q0": "q0",
    "F": ["q3"],
    "δ": {
        "(q0,0)": "q1",
        "(q0,1)": "q2",
        "(q1,0)": "q2",
        "(q1,1)": "q2",
        "(q2,0)": "q2",
        "(q2,1)": "q3",
        "(q3,0)": "q3",
        "(q3,1)": "q3",
        
    }
}


# # Generar el producto cruzado inicial
# initial_cross_product = cross_product_accept_not_accept(afn_example)
# print("Initial cross product:\n", initial_cross_product)

# # Encontrar los nuevos pares basados en las transiciones
# final_pairs = find_transition_pairs(afn_example, initial_cross_product)

# print("Final list of pairs:\n")
# print(final_pairs)

# # States X States
# print("States X states\n")
# states_product = cross_product_states(afn_example)
# print(states_product)

# # Calcular la diferencia
# difference = difference_between_lists(states_product, final_pairs)
# print("Difference:\n")
# print(difference)


# # Generar el nuevo autómata
# new_automaton = generate_reduced_automaton(afn_example, difference)
# if new_automaton:
#     print("New Automaton:\n", new_automaton)
    
#     # Exportar el autómata a un archivo JSON
#     with open('reduced_automaton.json', 'w') as json_file:
#         json.dump(new_automaton, json_file, indent=4)
#         print("El nuevo autómata ha sido exportado a 'reduced_automaton.json'.")