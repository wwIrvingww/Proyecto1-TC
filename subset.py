import copy
import json

# ---- Functions ---- #
# iterates through transi
# from an initial states through all epsilom transitions
def getLock(state, transitions):
    last = []
    lock = copy.deepcopy(state)
    while last!=lock:
        last = copy.deepcopy(lock)
        for ste in last:
            for key, item in transitions.items():
                tem = key.strip("()").split(",")
                if tem[0] == ste and tem[1]=='eps':
                    lock.extend([item for item in item if item not in lock])
    return lock

# Given a letter and a letters, it iterates through al transitions
# and it gives back all the results
def getTransition(state, letter, transitions):
    newState = []
    for ste in state:
        for key, item in transitions.items():
            tem = key.strip("()").split(",")
            if tem[0] == ste and tem[1]==letter:
                newState.extend([item for item in item if item not in newState])
    return newState

# calculate strating state and acceptance states
def getSpecialStates(keys, transitions):
    F = []
    q0 = ""
    start = str(getLock(['q0'],transitions))
    for i in keys.keys():
        if start == i:
            q0 = keys[i]
        if 'qf' in i:
            F.append(keys[i])
    return (q0, F)

# Subset main recursions
def subsetRecursion(initSate, states, transitions, set_transitions, alpha):
    # first it takes the lock of the starting value and that becomes the new
    # starting value for the recursion
    lock = getLock(initSate, transitions)
    # The starting value is appended to the states array and the array of not yet processed
    states.append(str(lock))
    notProcessed = [[], lock]
    while len(notProcessed)!=0: # While there are still states to process
        current = notProcessed.pop() # pops last not processed state
        for let in alpha: # iterate through letters
            newState = getTransition(current, let, transitions) # gets result of transition
            newLock=getLock(newState, transitions) # locks transition
            if newLock!=[]:
                if str(newLock) not in states: # adds new state to states
                    states.append(str(newLock))
                    notProcessed.append(newLock) # adds new lock to not processed
                # adds calculated transition to set transitions
                set_transitions[str(current)+"|"+let] = str(newLock)
            else: 
                # adds transition to empty state
                set_transitions[str(current)+"|"+let] = str([])
def make_renamed_states(set_to_state, set_states, renamed_states):
    counter = 0
    for i in set_states:
        renamed_states.append('s'+str(counter))
        set_to_state[i] = 's'+str(counter)
        counter+=1
    
def make_state_transitions(state_transitions, set_transitions, set_to_state):
    for i in set_transitions.keys(): # other states
        trans = i.split('|')
        state_transitions["("+set_to_state[trans[0]]+","+trans[1]+")"] = set_to_state[set_transitions[i]]
def set_main(afn):
    # Step 1: get transitions and alphabet from the afn
    transitions  = copy.deepcopy(afn['D'])
    alphabet = copy.deepcopy(afn['S'])
    # Step 2: make afd in set form
        # New states and new transitions from set agrupation start as empty
    set_states = []
    set_transitions = {}
        # Recursion starts with an array with only the starting state
    subsetRecursion(['q0'], set_states, transitions,set_transitions,alphabet)

    # Step 3: translate between set version to a more readable state version
        # a set to state dictionary is made to translate between 
        # states in set form and new named sets
    set_to_state = {"[]":"m"}
    renamed_states = ['m'] # will have the new states
    make_renamed_states(set_to_state, set_states, renamed_states)

    state_transitions = {} # will have transitions in the new state form
    make_state_transitions(state_transitions, set_transitions, set_to_state)
    
    # Step 4: find new initial state and new acceptance states
    spec = getSpecialStates(set_to_state, transitions)
    q0 = spec[0]
    F = spec[1]

    # Step 5: afd is built
    afd = {
        "Q": renamed_states,
        "S": alphabet,
        "q0": q0,
        "F": F,
        "D": state_transitions
    }
        
    return afd