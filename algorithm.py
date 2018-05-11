from tree2 import *

def find_X(node, path):
    if node.tag() == 'NP' or node.tag() == 'S':
        return node, path
    path.append(node)
    next_step = get_parent(node)
    return find_X(next_step, path)

# Condition three: 
# Traverse all branches below node X to the left of path p
# in a left-to-right, breadth-first fashion.
def explore(X, has_encountered_NP_or_S):
	# Traverse all branches, left-to-right, breadth-first
	if is_leaf(X):
		return []
	if X.tag() == 'NP' or X.tag() == 'S':
		is_NP_or_S = True

	to_explore = []
	if has_encountered_NP_or_S:
		if X.get_left().tag() == 'NP':
			to_explore.append(X.get_left())
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
	if is_leaf(X): return X
	if X.get_left() not in path:
		return X.get_left()
	return find_left_of_p(X.get_right(), path)

def steps_two_through_four(search_start, path):
    X, path = find_X(get_parent(search_start), path)
    node = find_left_of_p(X, path)
    return X, path, explore_left(X, path)

def explore_right_helper(X):
	if is_leaf(node): return []
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
	if is_leaf(X): return []
	if X.get_right() not in path:
		return explore_right_helper(X.get_right())
	return explore_right(X.get_left(), path)

def resolve_anaphor(input_node):
    # Begin at NP node immediately dominating pronoun
    search_start = get_parent(input_node)
    while search_start.tag() is not 'NP':
        search_start = get_parent(search_start)
    X, path, proposed_antecedents = \
    	steps_two_through_four(search_start, [])
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
        proposed_antecedents += explore(node, true)
        if X.tag() == 'S':
            proposed_antecedents += explore_right(X, path)
	    # Step 8: if X is an S node, traverse all branches of node
	    # X to the right of the path p in a left-to-right breadth-
	    # first meanner, but do not go below any NP or S node 
	    # encountered. Propose any NP node encountered as the 
	    # antecedent.
    return proposed_antecedents


