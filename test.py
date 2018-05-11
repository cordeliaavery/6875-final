from tree import Tree
from tree3 import process_string
from tree2 import Tree as Tree2
from tree2 import is_leaf
from algorithm import resolve_anaphor
import json

#resolve_anaphor(x)

with open("binding_dataset.neural.json") as f:
    parser_output = json.load(f)

for elem in sorted(parser_output["sentences"], key=lambda x: x["index"]):
    proc = process_string(elem["parse"])
    tree_to_parse = Tree2(proc[0])
    def look_for_PRP(cell):
        if cell is None: return []
        unresolved = []
        if cell.tag() == 'PRP':
            unresolved.append(cell)
        if cell.is_leaf(): return unresolved
        return unresolved + look_for_PRP(cell.get_left()) + look_for_PRP(cell.get_right())
    candidates = look_for_PRP(tree_to_parse)
    for candidate in candidates:
        proposed = resolve_anaphor(candidate)
        for proposal in proposed:
            proposal.pretty_print()

    # Search for PRP
    # If PRP found, send into algorithm to resolve anaphor
    tree_to_parse.pretty_print()
    break
