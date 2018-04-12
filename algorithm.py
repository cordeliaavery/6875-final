# from tree_structure_tbd import get_parent, get_left, get_right, is_tree, is_leaf

# X is from Hobbs paper, first NP or S encountered
# when going up the tree.
def find_X(node, path):
    if node.tag is 'NP' or node.tag is 'S':
        return node, path
    path.append(node)
    next_step = get_parent(node)
    return find_X(next_step, path)

def resolve_anaphor(node):
    # Begin at NP node immediately dominating pronoun
    search_start = get_parent(node)
    if search_start.tag is not 'NP':
        search_start = get_parent(node)
    X, path = find_X(search_start, [])
    proposed_antecedents = explore(X)
