from tree2 import *

def find_X(node, path):
    path.append(node)
    if node.tag() == 'NP' or node.tag() == 'S':
    #if node.tag().startswith('S'):
        return node, path
    next_step = get_parent(node)
    if next_step is None: return None, path 
    return find_X(next_step, path)

def explore_left_of_path(X, path, has_encountered_NP_or_S=False):
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

def explore_right(X, path):
    proposed = []
    queue = []
    if X.get_left() in path:
        queue.append(X.get_left())
    queue.append(X.get_right())
    # Explore each layer of the tree, adding to a queue!
    while len(queue) > 0:
        node = queue.pop(0)
        if node is None: continue
        if node not in path:
            if node.tag() == 'NP':
                proposed.append(node)
        if node.tag() == 'NP' or node.tag() == 'S': continue
        if not node.is_leaf():
            if node.get_left() in path:
                queue.append(node.get_left())
            queue.append(node.get_right())
    return proposed

def is_not_highest_S(X):
    if X is None: return False
    if X.tag() != 'S': return True
    while(get_parent(X) is not None):
        X = get_parent(X)
        if X.tag() == 'S':
            return True
    return False

#Placeholder because we don't know how to do this
def X_immediately_dominates_Nbar_in_path(X, path):
    return False

def resolve_anaphor(input_node):
    # Begin at NP node immediately dominating pronoun
    path = [input_node]
    search_start = get_parent(input_node)
    while True:
        path.append(search_start)
        if search_start.tag() == 'NP': break
        search_start = get_parent(search_start)
    X, path = find_X(get_parent(search_start), path)
    if X is None:
        return None
    proposed_antecedents = explore_left_of_path(X, path)
    while(is_not_highest_S(X)):
        # Step 5: From node X, go up the tree to the first
        # NP or S node encountered. Call this new node X, 
        # and call the path traversed to reach it p
        path.append(X)
        X = get_parent(X)
        X, path = find_X(X, path)
        #TODO: Fix this!
        # Step 6: If X is an NP node and if the path p to X 
        # did not pass through the N bar node that X immediately
        # dominates, propose X as the antecedent.
        if X.tag() == 'NP':
            if not X_immediately_dominates_Nbar_in_path(X, path):
                proposed_antecedents.append(X)

        # Step 7: Traverse all branches below node X to the left 
        # of path p in a left-to-right, breadth-first manner. 
        # Propose any NP node encountered as the antecedent
        proposed_antecedents += explore_left_of_path(X, path, True)


        # Step 8: if X is an S node, traverse all branches of node
        # X to the right of the path p in a left-to-right breadth-
        # first meanner, but do not go below any NP or S node 
        # encountered. Propose any NP node encountered as the 
        # antecedent.
        if X.tag() == 'S':
            proposed_antecedents += explore_right(X, path)
    return proposed_antecedents
    # Should explore previous sentences at this point


