# ----- CLASSES ----- #
# Tree node class
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# AF state class
class afstate:
    def __init__(self, name):
        self.name = name
        self.trans = []
    @classmethod
    def array_init(cls, array):
        # Create a new instance of afstate using the class constructor
        obj = cls(name='q'+str(len(array)-1))
        array.append('q'+str(len(array)-1))
        obj.trans = []  # Initialize trans to an empty list
        return obj
        
    def add(self, value):
        self.trans.append(value)

# ---- INTERMEDIARY FUNCTIONS ---- #

# Conversion from postfix format to tree
def postfix_to_tree(postfix, alphabet): 
    stack = []
    for token in postfix:
        if token in alphabet:  # If the token is in the alphabet, it pushes it onto the stack
            stack.append(TreeNode(token))
        else:  # If the token is an operator:
            if token !='*': # regular node appending
                node = TreeNode(token)
                node.right = stack.pop()
                node.left = stack.pop()
                stack.append(node)
            else: # for * operator, only last token is appended
                node = TreeNode(token)
                node.left = stack.pop()
                stack.append(node)
    return stack.pop()  # The root of the expression tree for processing

# Add transition as a list
def appendTrans(dict, key, val):
    try:
        dict[key].append(val)
    except:
        dict[key] = [val]
    
# iterates through nodes, and turns transitions into a dictionary
def node_to_dict(node, transitions):
    if node is not None:
        for tran in node.trans:
            tem_key = "("+node.name+","+tran[0]+")"
            tem_val = tran[1].name
            try:
                if tem_val not in transitions[tem_key]:
                    appendTrans(transitions, tem_key, tem_val)
                    node_to_dict(tran[1], transitions) 
            except:
                appendTrans(transitions, tem_key, tem_val)
                node_to_dict(tran[1], transitions) 

def nodeCase(right, left):
    if right.value in ['*','+','.'] and left.value in ['*','+','.']:
        # Both nodes are operators
        return 0
    elif right.value in ['*','+','.']:
        # Only right is operator
        return 1
    elif left.value in ['*','+','.']:
        # Only left is operator
        return 2
    else:
        # None are operator
        return 3

def make_afd(node, last_start, last_end,Q):
    if node.right is not None and node.left is not None:
        if node.value == '+':
            # Intiating states
            first = afstate.array_init(Q)
            second = afstate.array_init(Q)
            
            # Creates transitions for + operation
            first.trans.append(('eps' ,last_end))
            second.trans.append(('eps' ,last_end))
            
            # Depending on the case (letter or operation), how the last_start
            # is conected to first and second
            case = nodeCase(node.right, node.left)
            if case == 0: # Both Operators
                make_afd(node.right, last_start, first, Q)
                make_afd(node.left, last_start, second, Q)
            elif case == 1: # Right is operator
                last_start.trans.append((node.left.value,second)) 
                make_afd(node.right, last_start, first, Q)
            elif case == 2: # Left is operator
                last_start.trans.append((node.right.value,first))
                make_afd(node.left, last_start, second, Q)  
            else: # None operators
                last_start.trans.append((node.right.value,first))
                last_start.trans.append((node.left.value,second))

        elif node.value == '.':
            # Intiating states
            first = afstate.array_init(Q)
            second = afstate.array_init(Q)

            # Depending on the case (letter or operation), how the last_start
            # is conected to first and second
            case = nodeCase(node.right, node.left)
            
            if case == 0: # Both Operators
                second.trans.append(('eps',last_end))
                make_afd(node.left, last_start, first, Q)
                make_afd(node.right, first, second, Q)
            elif case == 1: # Right is operator
                last_start.trans.append((node.left.value,first))
                first.trans.append((node.right.value,second))
                make_afd(node.right, second, last_end, Q)
            elif case == 2: # Left is operator
                second.trans.append(('eps',last_end))
                first.trans.append((node.right.value,second))
                make_afd(node.left, last_start, first, Q)
            else: # None operators
                second.trans.append(('eps',last_end))
                last_start.trans.append((node.left.value,first))
                first.trans.append((node.right.value,second))
         
    elif node.left is not None:
        # Node only has one son at the left, meaning its a * operator
        if node.value == '*':
            # Connects start to end and viceversa
            last_start.trans.append(('eps',last_end))
            last_end.trans.append(('eps',last_start))
            # continues recursivenes form the son at the left
            make_afd(node.left, last_start, last_end, Q)
    elif node is not None:
        # if theres a number that doesnt have siblings
        # Means its the only son of a * operator
        mid = afstate.array_init(Q)
        last_start.trans.append((node.value,mid))
        mid.trans.append(('eps',last_end))
            

def thomspon_main(infix, alphabet):
    transitions = {}
    root = postfix_to_tree(infix,alphabet)
    start = afstate("q0")
    end = afstate("qf")
    Q = [start.name,end.name] 
    F = [end.name]
    q0 = start.name
    make_afd(root, start, end, Q)
    node_to_dict(start, transitions)
    afd = {
        "Q": Q,
        "S": alphabet,
        "q0": q0,
        "F": F,
        "D": transitions
    }
    return afd