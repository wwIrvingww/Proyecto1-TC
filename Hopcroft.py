import itertools

def cross_product_accept_not_accept(afn):
    states = afn["Q"]
    accepting_states = afn["F"]
    non_accepting_states = [state for state in states if state not in accepting_states]
    cross_product = list(itertools.product(accepting_states, non_accepting_states))
    return cross_product

def find_transition_pairs(afn, cross_product):
    transitions = afn["δ"]
    alphabet = afn["Σ"]
    
    new_pairs = set(tuple(sorted(pair)) for pair in cross_product)  # Ordena los pares al agregarlos al set

    while True:
        added_new_pairs = False
        
        current_pairs = list(new_pairs)
        for (q_accept, q_non_accept) in current_pairs:
            for symbol in alphabet:
                q_accept_from = None
                q_non_accept_from = None
                
                for (key, value) in transitions.items():
                    state, transition_symbol = key.strip("()").split(',')
                    state = state.strip()
                    transition_symbol = transition_symbol.strip()

                    if transition_symbol == symbol:
                        if value == q_accept:
                            q_accept_from = state
                        if value == q_non_accept:
                            q_non_accept_from = state
                
                if q_accept_from and q_non_accept_from:
                    new_pair = tuple(sorted((q_accept_from, q_non_accept_from)))
                    if new_pair not in new_pairs:
                        new_pairs.add(new_pair)
                        added_new_pairs = True
                        print(f"Added new pair: {new_pair}")

        if not added_new_pairs:
            break

    return list(new_pairs)

# Example usage with the sample AFN
afn_example = {
    "Q": ["s", "q1", "q2", "q3"],
    "Σ": ["a", "b"],
    "q0": "s",
    "F": ["q3"],
    "δ": {
        "(s,a)": "q1",
        "(s,b)": "q3",
        "(q1,a)": "q2",
        "(q1,b)": "s",
        "(q2,a)": "q2",
        "(q2,b)": "q3",
        "(q3,a)": "q2",
        "(q3,b)": "q2"
    }
}

initial_cross_product = cross_product_accept_not_accept(afn_example)
print(initial_cross_product)

final_pairs = find_transition_pairs(afn_example, initial_cross_product)

print("Final list of pairs:")
print(final_pairs)
