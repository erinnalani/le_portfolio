# Ling 571 HW5
import sys
from collections import defaultdict
from pprint import pprint
from nltk import Nonterminal


def make_ddict(p):
    '''
    Makes dict to store information on relations between words.
    Key = word index.
    Value = list containing word, relation, and head index.
    '''
    
    # Init dependency dict
    dep_dict = defaultdict(None)
    
    # Preprocess lines in parse
    relations = p.split('\n')
    for relation in relations:
        parts = relation.strip().split('\t')
        
        # Create parse dict
        dep_dict[parts[0]] = [item for item in parts[1:]]

    return dep_dict


    
def consult_oracle(dep_dict):
    '''
    Implements oracle function using dependency dictionary.
    Updates stack and buffer throughout.
    Stores output results in arcs and transitions lists.
    '''

    # Init config and transitions list
    stack = []
    buffer = []
    arcs = []
    transitions = []

    # Extract sentence for buffer
    for i in range(1, len(dep_dict) + 1):
        word = dep_dict[str(i)][0]
        buffer.append(word)

    # Finalize buffer  
    buffer = [elem for elem in enumerate(buffer, 1)]

    
    # Add root to stack
    stack.append(tuple((0, 'ROOT')))

    # Start implementation
    while len(buffer) != 0:
        if len(stack) < 3: # Covers if stack is ROOT or only has 2 elem
            shift(stack, buffer)
            
            # Add transition to transition list
            transitions.append(('SHIFT'))
            
        else:
            # Check for left arc
            if check_LA(stack, dep_dict):
                # Make left arc
                make_LA(arcs, dep_dict, stack, transitions)
                
            elif check_RA(stack, dep_dict, buffer):
                # Make right arc
                make_RA(arcs, dep_dict, stack, transitions)
                
            else:
                # Words have no relation
                # Shift
                shift(stack, buffer)

                # Add transition to transition list
                transitions.append('SHIFT')
    
    # When no words left in buffer
    while len(buffer) == 0:
        if len(stack) == 2: # Only root and 1 word
            # Connect final word to ROOT
            make_RA(arcs, dep_dict, stack, transitions)

        elif len(stack) == 1: # only root
            # End of graph
            # Output results
            output_transitions(transitions)
            output_arcs(arcs)
            break
        else:
            # Check for left arc
            if check_LA(stack, dep_dict):
                # Make left arc
                make_LA(arcs, dep_dict, stack, transitions)

            elif mod_check_RA(stack, dep_dict):
                # Make right arc
                make_RA(arcs, dep_dict, stack, transitions)
        


def shift(stack, buff):
    '''
    Implements SHIFT transition, updating the stack and buffer lists
    '''
    curr_word = buff.pop(0)
    stack.append(curr_word)


def check_LA(stk, d_dict):
    '''
    Checks if relationship between words in stack constitutes a left arc. 
    Returns T if it's a left arc.
    '''
    top = stk[-1] # Top of stack
    bottom = stk[-2] # 2nd elem of stack


    if d_dict[str(bottom[0])][2] == str(top[0]): # if the index of top word matches head of bottom word (in dict)
        return True
    else:
        return False



def check_RA(stk, d_dict, buff):
    '''
    Checks if relationship between words in buffer constitutes a right arc.
    Runs a check for whether top of stack has any dependents. 
    Returns T if it's a right arc and word has no dependents in buffer.
    '''
    top = stk[-1] # Top of stack
    bottom = stk[-2] # 2nd elem of stack

    if d_dict[str(top[0])][2] == str(bottom[0]):  # if the index of bottom word matches head of top word (in dict)
        if not check_RA_deps(stk, d_dict, buff): # if word has no dependents
            return True # is RA
        return False

    

def check_RA_deps(stk, d_dict, buff):
    '''
    Checks whether or not remaining words in buffer are dependents of
    word at top of stack.
    Returns True if top of stack has dependents.'''

    for word in buff:
        if d_dict[str(word[0])][2] == str(stk[-1][0]):
            return True
    
    return False


def make_LA(arc_list, d_dict, stk, trans_list):
    '''
    Adds left arc to arcs list in tuple form.
    Adds transition LEFFARC and label to transitions list
    '''

    dep = stk.pop(-2) # Remove from stack
    head = stk[-1] # Keep on stack

    # Add dependent to temp list for arc contents
    arc_info = [elem for elem in dep]
    
    # Add label
    label = Nonterminal(d_dict[str(dep[0])][1])
    arc_info.append(label)
    
    # Add head index
    arc_info.append(str(head[0]))

    # Add to arcs list and transitions list
    arc_list.append(tuple(arc_info))
    trans_info = []
    trans = Nonterminal('LEFTARC')
    trans_info.append(trans)
    trans_info.append(label)

    trans_list.append(tuple(trans_info))




def make_RA(arc_list, d_dict, stk, trans_list):
    '''
    Adds right arc to arcs list in tuple form.
    Adds transition RIGHTARC to transitions list.
    '''
    dep = stk.pop()
    head = stk[-1]
    
    # Add dependent to temp list for arc contents
    arc_info = [elem for elem in dep]

    # Add label
    label = Nonterminal(d_dict[str(dep[0])][1])
    arc_info.append(label)

    # Add head index
    arc_info.append(str(head[0]))

    # Add to arcs list and transitions list
    arc_list.append(tuple(arc_info))
    trans_info = []
    trans = Nonterminal('RIGHTARC')
    trans_info.append(trans)
    trans_info.append(label)

    trans_list.append(tuple(trans_info))

def mod_check_RA(stk, d_dict):
    '''
    Modified version of check_RA() - doesn't check buffer b/c 
    this only runs if buffer is emtpy.
    Checks if relationship between words in stack = right arc.
    Returns T if it's a right arc.
    '''
    top = stk[-1] # Top of stack
    bottom = stk[-2] # 2nd elem of stack

    if d_dict[str(top[0])][2] == str(bottom[0]):  # if the index of bottom word matches head of top word (in dict)
        return True
    return False



def output_transitions(trans_list):
    with open(output_seqs, 'a', encoding='utf8') as f:
        # Output
        for trans in trans_list:
            f.write(f'{trans}\n')
        f.write('\n')
    

def output_arcs(arcs_list):
    with open(output_deps, 'a', encoding='utf8') as f:
        # Sort by index
        sorted_arcs = sorted(arcs_list, key=lambda x: x[0])
        # Output
        for arc in sorted_arcs:  
            f.write(f'{arc[0]}\t{arc[1]}\t{arc[2]}\t{arc[3]}\n')
        f.write('\n')




if __name__=="__main__":

    try:
        # Define input and output files
        input_deps = sys.argv[1]
        output_deps = sys.argv[2]
        output_seqs = sys.argv[3]

        # Read in input dependencies
        with open(input_deps, 'r', encoding='utf8') as f:
            in_deps = f.read()

            # Group dependency parses
            d_parses = in_deps.strip().split("\n\n")

            for parse in d_parses:

                # Create dependency dict
                d_dict = make_ddict(parse)

                # Implement oracle
                consult_oracle(d_dict)

    except OSError as e:
        print(e)




        
    