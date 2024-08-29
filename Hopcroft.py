import itertools

def cross_product_accept_not_accept(afn):
    # Extracting the states and accepting states from the AFN
    states = afn["Q"]
    accepting_states = afn["F"]
    
    # Identifying non-accepting states
    non_accepting_states = [state for state in states if state not in accepting_states]
    
    # Compute the cross product of accepting states x non-accepting states
    cross_product = list(itertools.product(accepting_states, non_accepting_states))
    
    # Print the cross product
    print("Cross Product of Accepting States x Non-Accepting States:")
    for pair in cross_product:
        print(pair)
    
    return cross_product


afn_example = {
    "Q": ["s", "q1", "q2", "q3"],
    "Σ": ["a", "b"],
    "q0": "s",
    "F": ["q3", "q2"],
    "δ": {
        "(s,a)": "q1",
        "(s,b)": "q3",
        "(q1,a)": "q2",
        "(q1,b)": "s",
        "(q2,a)": "q2",
        "(q2,b)": "q2",
        "(q3,a)": "q2",
        "(q3,b)": "q2"
    }
}


cross_product_list = cross_product_accept_not_accept(afn_example)
