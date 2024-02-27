import sys
import nltk
from nltk import word_tokenize
import numpy as np
from collections import defaultdict
from pprint import pprint


# Init grammar dict
CNF_DICT = defaultdict(list)


   
def make_grammar_dict(gr):
     """
    Create dictionary for CNF grammar to map RHS of
    productions to corresponding LHS.
    LHS are kept in a set to avoid duplicates
    """
     for prod in gr.productions():
        # Handle new key
        if prod.rhs() not in CNF_DICT:
            CNF_DICT[prod.rhs()] = set()
        # Add LHS to dict   
        CNF_DICT[prod.rhs()].add(prod.lhs())


def init_table(n_dim):
    """Init table for storing subtrees based on spans between words in the sentence.
    Dimensions are (n + 1)^2 to correcspond with the spans between words:
     e.g. the first preterminal is at span (0,1), so the subtree is at table[0][1]"""
    
    table = np.empty((n_dim + 1, n_dim + 1), dtype=object)
    
    # Add list container to each cell
    for i in range(n_dim + 1):
        for j in range(n_dim + 1):
            table[i][j] = []
    
    # Print check for map_table
    # for row in table:
    #     print([item.tolist() if isinstance(item, np.ndarray) else item for item in row])
    
    return table


def add_subtree(tbl, i, k, end):
    """
        Add subtree to current cell based on the span [i, end] and k split
    """

    for sub1 in tbl[i, k]:
        for sub2 in tbl[k, end]:
            rhs = (sub1.label(), sub2.label())
            if rhs in CNF_DICT:
                lhs = CNF_DICT[rhs]
                for NT in lhs:
                    tbl[i, end].append(nltk.Tree(NT, [sub1, sub2]))
    return tbl



def cky_parse(words, grammar):
    """ 
        Parse sentence using CNF grammar and CKY algorithm.
        Process:
        Parse is performed diagonally starting from [0,1] with PTs
        lastly, filling each column bottom to top, ending with the 
        start symbol at [0,8]. Each 2 adjacent cells (diagonally) 
        are built upon with there parent subtree filled in in the
        next diagonal row before moving down the diagonal.
    """
    
    # Get length of sentence
    n = len(words)
    # print(f'LOOK: {words[1]}')

    # Add grammar rules to dict
    make_grammar_dict(grammar)
    # pprint(CNF_DICT)

    # Make map_table
    map_table = init_table(n)
    # print(map_table)

    # Start parse
    for end in range(1, n + 1):  # Traverse by diagonal
        terminal = tuple([words[end - 1]])
 
        # Fill in terminals
        if terminal in CNF_DICT:
            for NT in CNF_DICT[terminal]:
                map_table[end - 1][end].append(nltk.Tree(NT, [words[end-1]])) # add final subtree to cell
                   
        for i in range(end - 2, -1, -1): # Define vertical range
            for k in range(i + 1, end): # Define split point
                # Fill in other NTs
                map_table = add_subtree(map_table, i, k, end)
            

    # # Print check for map_table
    # for row in map_table:
    #     print([item.tolist() if isinstance(item, np.ndarray) else item for item in row])

    return map_table


def output_result(trees, sentence):

    # Init parse count
    parse_count = 0

    with open(output_file, 'a', encoding='utf8') as f:
        # Output sentence
        f.write(f'{sentence}')

        # Print all trees in list 
        for tree in trees:
            f.write(f'{tree}\n')
            parse_count += 1
        
        # Output num of parses
        f.write(f'Number of parses: {parse_count}\n')
        f.write('\n')





if __name__=="__main__":
    try:
        # Load grammar and read in files
        grammar = sys.argv[1]
        sentences = sys.argv[2]
        output_file = sys.argv[3]

        cnf = nltk.data.load(grammar)
        make_grammar_dict(cnf)

        pprint(CNF_DICT)

        with open (sentences, 'r', encoding='utf8') as f:
            # Read in sentences
            sents = f.readlines()

            for sent in sents:
                words = word_tokenize(sent)
            # print(words)
                n = len(words)
            # print(n)
            
                # Parse & get subtrees
                subtree_table = cky_parse(words, cnf)
                
                # Send final trees to output
                tree_list = [tree for tree in subtree_table[0][n]]
                output_result(tree_list, sent)



                
               
                

            # Print check for map_table
            # for row in subtree_table:
            #     print([item.tolist() if isinstance(item, np.ndarray) else item for item in row])
           



    except OSError as e:
        print(e)