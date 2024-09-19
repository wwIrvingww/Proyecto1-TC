import itertools

def initial_partition(afd):
    """Create the initial partition: accepting and non-accepting states"""
    accepting_states = set(afd["F"])
    non_accepting_states = set(afd["Q"]) - accepting_states
    
    # Create the initial partition
    partitions = [accepting_states, non_accepting_states]
        
    return partitions

def refine_partitions(afd, partitions):
    """Refine the partitions based on the transitions of the DFA"""
    alphabet = afd["Σ"]
    transitions = afd["δ"]
    
    new_partitions = partitions[:]
    worklist = partitions[:]

    while worklist:
        A = worklist.pop(0)  # Pick the first set from the worklist

        for symbol in alphabet:
            # Find all states that transition into A on this symbol
            X = {state for state in afd["Q"] if afd["δ"].get(f"({state},{symbol})", None) in A}

            # Refine each partition based on X
            updated_partitions = []
            for Y in new_partitions:
                Y1 = Y & X  # States in Y that transition into A on symbol
                Y2 = Y - X  # States in Y that don't transition into A on symbol

                if Y1 and Y2:  # If we can split the partition
                    new_partitions.remove(Y)
                    new_partitions.append(Y1)
                    new_partitions.append(Y2)

                    # Add the smaller partition to the worklist
                    if Y1 in worklist or Y2 in worklist:
                        worklist.remove(Y1 if Y1 in worklist else Y2)
                    worklist.append(Y1 if len(Y1) <= len(Y2) else Y2)

                updated_partitions.append(Y1 or Y2)
    
    return new_partitions

def assign_state_names(partitions):
    """Assign unique names to each partition in the minimized DFA"""
    state_mapping = {}
    state_counter = 0
    
    for partition in partitions:
        state_name = f"S{state_counter}"
        state_mapping[frozenset(partition)] = state_name
        state_counter += 1
    
    return state_mapping

def create_minimized_dfa(afd, partitions):
    """Create a minimized DFA based on the refined partitions"""
    # Assign unique names to each partition
    state_mapping = assign_state_names(partitions)
    
    # Generate minimized states
    minimized_states = list(state_mapping.values())
    minimized_transitions = {}

    # Create the minimized transition function
    for part in partitions:
        if not part:  # Skip empty partitions
            continue
        representative = next(iter(part))  # Pick any state from the partition as representative
        for symbol in afd["Σ"]:
            target = afd["δ"].get(f"({representative},{symbol})", None)
            if target is not None:
                # Ensure the target is part of some partition
                target_partition = None
                for p in partitions:
                    if target in p:
                        target_partition = p
                        break

                if target_partition is not None:
                    minimized_transitions[f"({state_mapping[frozenset(part)]},{symbol})"] = state_mapping[frozenset(target_partition)]
    
    # Get minimized start state and accepting states
    start_partition = None
    for part in partitions:
        if afd["q0"] in part:
            start_partition = part
            break
    
    if start_partition is None:
        raise ValueError(f"El estado inicial '{afd['q0']}' no se encontró en ninguna partición.")
    
    minimized_start_state = state_mapping[frozenset(start_partition)]
    minimized_accept_states = [state_mapping[frozenset(part)] for part in partitions if any(state in afd["F"] for state in part)]

    return {
        "Q": minimized_states,
        "Σ": afd["Σ"],
        "q0": minimized_start_state,
        "F": minimized_accept_states,
        "δ": minimized_transitions
    }


def hopcroft_minimization(afd):
    """Main function for Hopcroft's DFA minimization"""
    # Step 1: Initial partition (accepting and non-accepting states)
    partitions = initial_partition(afd)
    
    # Step 2: Refine partitions
    final_partitions = refine_partitions(afd, partitions)
    
    # Step 3: Create the minimized DFA with named states
    minimized_dfa = create_minimized_dfa(afd, final_partitions)
    
    return minimized_dfa
