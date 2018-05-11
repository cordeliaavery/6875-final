from tree2 import *

def find_X(node, path):
    path.append(node)
    if node.tag() == 'NP' or node.tag() == 'S':
        return node, path
    next_step = get_parent(node)
    return find_X(next_step, path)

def explore_left_of_path(X, path):
    has_encountered_NP_or_S = False
    proposed = []
    queue = [(X.get_left(), has_encountered_NP_or_S)]
    if X.get_right() in path:
        queue.append((X.get_right(), has_encountered_NP_or_S))
    # Explore each layer of the tree, adding to a queue!
    while len(queue) > 0:
        node, has_encountered_NP_or_S = queue.pop(0)
        if node is None: continue
        if node not in path:
            if has_encountered_NP_or_S:
                if node.tag() == 'NP':
                    proposed.append(node)
        if node.tag() == 'NP' or node.tag() == 'S': has_encountered_NP_or_S = True
        if not node.is_leaf():
            queue.append((node.get_left(), has_encountered_NP_or_S))
            if node.get_right() in path:
                queue.append((node.get_right(), has_encountered_NP_or_S))
    return proposed


# Condition three: 
# Traverse all branches below node X to the left of path p
# in a left-to-right, breadth-first fashion.
def explore(X, has_encountered_NP_or_S):
    # Traverse all branches, left-to-right, breadth-first
    if X is None or X.is_leaf():
        return []
    if X.tag() == 'NP' or X.tag() == 'S':
        is_NP_or_S = True

    to_explore = []
    if has_encountered_NP_or_S:
        if X.get_left() is not None:
            if X.get_left().tag() == 'NP':
                to_explore.append(X.get_left())
        if X.get_right() is not None:
            if X.get_right().tag() == 'NP':
                to_explore.append(X.get_right())
    if X.tag() == 'NP' or X.tag() == 'S':
        has_encountered_NP_or_S = True
    left_path = explore(X.get_left(), has_encountered_NP_or_S)
    right_path = explore(X.get_right(), has_encountered_NP_or_S)
    return to_explore + left_path + right_path

# Condition three: 
# Traverse all branches below node X to the left of path p
# in a left-to-right, breadth-first fashion.
def find_left_of_p(X, path):
    if X.is_leaf(): return X
    if X.get_left() not in path:
        return X.get_left()
    return find_left_of_p(X.get_right(), path)

def steps_two_through_four(search_start, path):
    X, path = find_X(get_parent(search_start), path)
    node = find_left_of_p(X, path)
    return X, path, explore(X, False)

def explore_right_helper(X):
    if X is None: return []
    if X.is_leaf(): return []
    to_explore = []
    if X.get_left().tag() == 'NP':
        to_explore.append(X.get_left())
    if X.get_right().tag() == 'NP':
        to_explore.append(X.get_right())
    if (X.get_left().tag() == 'NP' or X.get_left().tag() == 'S' or 
        X.get_right().tag() == 'NP' or X.get_right().tag() == 'S'):
        return to_explore
    return (to_explore + explore_right_helper(X.get_left()) + 
            explore_right_helper(X.get_right()))


def explore_right(X, path):
    if X is None: return []
    if X.is_leaf(): return []
    if X.get_right() not in path:
        return explore_right_helper(X.get_right())
    return explore_right(X.get_left(), path)

def resolve_anaphor(input_node):
    # Begin at NP node immediately dominating pronoun
    path = [input_node]
    search_start = get_parent(input_node)
    while True:
        path.append(search_start)
        if search_start.tag() == 'NP': break
        search_start = get_parent(search_start)
    search_start.pretty_print()
    X, path = find_X(get_parent(search_start), path)
    proposed_antecedents = explore_left_of_path(X, path)
    print proposed_antecedents
    while(get_parent(X) is not None):
        # Step 5: From node X, go up the tree to the first
        # NP or S node encountered. Call this new node X, 
        # and call the path traversed to reach it p
        X_old = X
        X, path = find_X(X, path)
        #TODO: Fix this!
        # Step 6: If X is an NP node and if the path p to X 
        # did not pass through the N bar node that X immediately
        # dominates, propose X as the antecedent.
        if X.tag() == 'NP': 
            if input_node not in path:
                proposed_antecedents.append(X)
        # Step 7: Traverse all branches below node X to the left 
        # of path p in a left-toright, breadth-first manner. 
        # Propose any NP node encountered as the antecedent
        node = find_left_of_p(X, path)
        proposed_antecedents += explore(node, True)
        if X.tag() == 'S':
            proposed_antecedents += explore_right(X, path)
        X = get_parent(X)
        # Step 8: if X is an S node, traverse all branches of node
        # X to the right of the path p in a left-to-right breadth-
        # first meanner, but do not go below any NP or S node 
        # encountered. Propose any NP node encountered as the 
        # antecedent.
    return proposed_antecedents


