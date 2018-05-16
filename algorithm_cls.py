from tree2 import *
import re

# want to traverse to the nearest node to determine C-command
HEADS = {'NP', 'S', 'VP'}


"""
node: target node

return: whether or not this node is a genitive case
"""
def is_genitive(node):
    if not node.config():
        # must explicitly licensed
        return False

    if node.config()["case"] == "gen":
        # if this is the only possible case, assume true
        return True
    elif re.search("gen", node.config()["case"]):
        # otherwise, have to verify that it's genitive
        assert (node.tag() == "NP")
        return node.parent() and node.parent().tag() == "NP"


"""
pro:  target node
ante: potential antecedent

return: boolean indicating whether the feature specifications are consistent
"""
def match(pro, ante):
    if not pro:
        # if not pass a base node, assume they match
        return True

    c1 = pro.config()
    c2 = ante.config()
    if not c1 or not c2:
        # if both nodes are specified, they must have valid configs
        return False

    for param in ["gender", "person", "count"]:
        # forces agreement via regex match
        if not re.search(c1[param], c2[param]):
            return False

    for param in ["animate"]:
        # selectional constraints are implemented
        # using booleans, default set to false
        if c1.get(param, False) != c2.get(param, False):
            return False
            #feature checking
            #continue

    return True


"""
node:     current governor
base:     target node we want to match
passed_S: if the target base is not within the smallest S (only match R-expressions)
heads:    head type to match, default includes NP, VP, S
included_non_matches: match all types of head as opposed to ones with agreement

returns: set of nodes governed by node, of type head, matching base
"""
def get_governed_nodes(node, base, passed_S=False, heads=HEADS, include_non_matches=False):
    # nodes governed by this node, not including base node
    # to get nodes c-commanded by a node, pass in node's parent, with base=node
    govs = set()
    for n in node.get_children():
        if n == base:
            continue

        if n.tag() in heads and \
           (include_non_matches or \
            match(base, n)) and \
           (n.config() and \
            ((not passed_S  and n.config()["type"] != "A") or \
             n.config()["type"] == "R")) and \
           not is_genitive(n):
            # only add heads of the target type
            # that match the target features
            # whose config is specified
            # and where binding conditions apply

            govs.add(n)

        # recurse on n's child nodes
        # need to search past S nodes to find R expressions
        govs |= get_governed_nodes(n,
                                   base,
                                   passed_S or n.tag() == 'S',
                                   heads,
                                   include_non_matches)

    return govs
        

"""
node:  current node
r_exp: if target is an expression
base:  target node
heads: head types to match

return: set of nodes that C-command current node that match base, if specified
"""
def get_c_commanding_nodes(node, r_exp=False, base=None, heads=HEADS):
    # nodes that c-command this node

    c_commands = set()

    # if node.type != R, only have to iterate
    # to the nearest S node
    #while node.parent() and node.parent().tag() not in HEADS:
    #    node = node.parent()

    if node.parent():
        for n in node.parent().get_children():
            if n != node and n.tag() in heads and match(base, n):
                c_commands.add(n)

        if node.parent().tag() != 'S' or r_exp:
            # want to make this a general function
            # R-expressions cannot be bound at all
            return c_commands | get_c_commanding_nodes(node.parent(),
                                                       base=base,
                                                       heads=heads)

    return c_commands


"""
node:   target node
NP_set: set of all NP nodes in the current sentence

return: set of possible antecedents for node
"""
def resolve_anaphor(node, NP_set):
    # Begin at NP node immediately dominating pronoun

    assert (node.tag() == "NP" and node.config())
    c_commanding = set()

    node_type = node.config()["type"]
    if node_type != "A":
        # assume pronouns and R-expressions can refer to everything
        # and eliminate candidates based on c-command
        synset = set(filter(lambda x: match(node, x) and x.parent() != node, NP_set))
        c_node = node
        while c_node:
            synset -= {c_node,}
            c_node = c_node.parent()

    if not node.parent():
        print "Invalid syntax--must have top-level S node!"
        exit(1)

    if not is_genitive(node) or node_type != "P":
        # check c-commanding nodes if node is not genitive pronoun

        # genitive pronouns can be bound, (i.e., "their")
        # genitive reflexives (i.e., "each other's") still must be bound
        # genitive R-expressions still cannot be bound

        c_commanding = get_c_commanding_nodes(node,
                                              base=node,
                                              r_exp = (node_type == "R"),
                                              heads={"NP",})


    # also want to eliminate bad coreferences lower
    # in the sentence (i.e, in  "he likes him", he != him,
    # while in "his brother likes him", his and him can corefer)
    governed = get_governed_nodes(node.parent(),
                                  node,
                                  heads={"NP",})

        
    if node_type == "A":
        # in the current implementation, these sets will
        # always be distinct, however, may want to have
        # long-distance control in the future
        return c_commanding - governed

    else:
        return (synset - c_commanding) - governed
