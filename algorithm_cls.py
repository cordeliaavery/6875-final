from tree2 import *
import re

# want to traverse to the nearest node to determine C-command
HEADS = {'NP', 'S', 'VP'}

def match(pro, ante):
    if not pro:
        return True

    c1 = pro.config()
    c2 = ante.config()
    if not c1 or not c2:
        return True

    for param in ["gender", "person", "count"]:
        # forces agreement
        if not re.search(c1[param], c2[param]):
            return False

    return True

def get_governed_nodes(node, base, passed_S=False, heads=HEADS, include_non_matches=False):
    # should just have to go up one level
    govs = set()
    for n in node.get_children():
        if n == base:
            continue
        if n.tag() in heads and (include_non_matches or match(n, base)) and (not passed_S or n.config()["type"] == "R"):
            govs.add(n)
        govs |= get_governed_nodes(n,
                                   base,
                                   passed_S or n.tag() == 'S',
                                   heads,
                                   include_non_matches)

    return govs
        

def get_c_commanding_nodes(node, r_exp=False, base=None, heads=HEADS):
    c_commands = set()

    # if node.type != R, only have to iterate
    # to the nearest S node
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



def resolve_anaphor(node, NP_set):
    # Begin at NP node immediately dominating pronoun

    assert (node.tag() == "NP" and node.config())

    node_type = node.config()["type"]
    if node_type == "P":
        # assume pronouns can refer to everything
        # and eliminate based on c-command
        synset = set(filter(lambda x: match(node, x), NP_set))
        c_node = node
        while c_node:
            synset -= {c_node,}
            c_node = c_node.parent()

    if node.parent():
        c_commanding = get_c_commanding_nodes(node,
                                              base=node,
                                              heads={"NP",})

        governed = get_governed_nodes(node.parent(),
                                      node,
                                      heads={"NP",})

    else:
        print "Invalid syntax--must have top-level S node!"
        exit(1)
        
    if node_type == "P":
        return (synset - c_commanding) - governed

    elif node_type == "A":
        print node_type
        return c_commanding - governed
    
