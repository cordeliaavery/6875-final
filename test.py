from tree import Tree
from tree3 import process_string
from tree2 import Tree as Tree2, get_index
from tree2 import is_leaf
from algorithm import resolve_anaphor
import json


with open("binding_dataset.neural.json") as f:
    parser_output = json.load(f)

for elem in sorted(parser_output["sentences"], key=lambda x: x["index"]):
    proc = process_string(elem["parse"])
    tree_to_parse = Tree2(proc[0])
    print tree_to_parse.get_string()
    tree_to_parse.pretty_print()
    #print get_index("John", tree_to_parse)
    def look_for_PRP(cell):
        if cell is None: return []
        unresolved = []
        if cell.tag() == 'PRP':
            unresolved.append(cell)
        if cell.is_leaf(): return unresolved
        #return unresolved + [look_for_PRP(x) for x in cell.get_children()]  #look_for_PRP(cell.get_left()) + look_for_PRP(cell.get_right())
        return unresolved + look_for_PRP(cell.get_left()) + look_for_PRP(cell.get_right())
    candidates = look_for_PRP(tree_to_parse)
    for candidate in candidates:
        proposed = resolve_anaphor(candidate)
        print 'Proposed antecedents for', candidate.get_string()

        print 'Are as follows: '
        if proposed is None:
            continue
        for proposal in proposed:
            proposal.pretty_print()
    print '-'*20    

    # Search for PRP
    # If PRP found, send into algorithm to resolve anaphor

