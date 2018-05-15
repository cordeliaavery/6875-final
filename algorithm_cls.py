from tree2 import *
import re

# want to traverse to the nearest node to determine C-command
HEADS = {'NP', 'S', 'VP'}

def is_genitive(node):
    if not node.config():
        return False
    if node.config()["case"] == "gen":
        return True
    elif re.search("gen", node.config()["case"]):
        assert (node.tag() == "NP")
        return node.parent() and node.parent().tag() == "NP"

def match(pro, ante):
    if not pro:
        return True

    c1 = pro.config()
    c2 = ante.config()
    if not c1 or not c2:
        return False

    for param in ["gender", "person", "count"]:
        # forces agreement
        if not re.search(c1[param], c2[param]):
            return False

    for param in ["animate"]:
        if c1.get(param, False) != c2.get(param, False):
            return False

    return True

def get_governed_nodes(node, base, passed_S=False, heads=HEADS, include_non_matches=False):
    # nodes governed by this node
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
            govs.add(n)
        govs |= get_governed_nodes(n,
                                   base,
                                   passed_S or n.tag() == 'S',
                                   heads,
                                   include_non_matches)

    return govs
        

def get_c_commanding_nodes(node, r_exp=False, base=None, heads=HEADS):
    # nodes that c-command this node

    c_commands = set()

    # if node.type != R, only have to iterate
    # to the nearest S node
    while node.parent() and node.parent().tag() not in HEADS:
        node = node.parent()

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
    c_commanding = set()

    node_type = node.config()["type"]
    if node_type != "A":
        # assume pronouns can refer to everything
        # and eliminate based on c-command
        synset = set(filter(lambda x: match(node, x) and x.parent() != node, NP_set))
        c_node = node
        while c_node:
            synset -= {c_node,}
            c_node = c_node.parent()

    if node.parent():
        if not is_genitive(node) or node_type != "P":
            c_commanding = get_c_commanding_nodes(node,
                                                  base=node,
                                                  r_exp = (node_type == "R"),
                                                  heads={"NP",})

        
        governed = get_governed_nodes(node.parent(),
                                      node,
                                      heads={"NP",})

    else:
        print "Invalid syntax--must have top-level S node!"
        exit(1)
        
    if node_type != "A": #node_type == "P":
        return (synset - c_commanding) - governed

    elif node_type == "A":
        return c_commanding - governed
    
    else:
        print "R-expression case not handled"
        exit(1)
