import json

def create_dfa_json():
    # Step 1: Input DFA components from the user
    
    # Input states
    states = input("Enter the states (comma-separated): ").split(',')
    states = [state.strip() for state in states]
    
    # Input alphabet
    alphabet = input("Enter the alphabet (comma-separated): ").split(',')
    alphabet = [symbol.strip() for symbol in alphabet]
    
    # Input initial state
    initial_state = input("Enter the initial state: ").strip()
    
    # Input accepting states
    accepting_states = input("Enter the accepting states (comma-separated): ").split(',')
    accepting_states = [state.strip() for state in accepting_states]
    
    # Input transitions
    transitions = {}
    print("Enter the transition function:")
    for state in states:
        for symbol in alphabet:
            next_state = input(f"Transition from ({state},{symbol}): ").strip()
            transitions[f"({state},{symbol})"] = next_state
    
    # Step 2: Construct the DFA dictionary
    dfa = {
        "Q": states,
        "Σ": alphabet,
        "q0": initial_state,
        "F": accepting_states,
        "δ": transitions
    }
    
    # Step 3: Convert dictionary to JSON string
    dfa_json = json.dumps(dfa, indent=2)
    
    # Step 4: Print or return the JSON string
    print("Generated DFA JSON:")
    print(dfa_json)
    
    return dfa_json

# Example usage
dfa_json_str = create_dfa_json()
