import re

class NodeError(Exception):
    def __init__(self, expression):
        self.expression = expression
        self.message = "Attempting to access child at leaf!"

class Tree:
    lexicon = None
    NP_nodes = set()
    PR_nodes = set()

    def __init__(self, vals, root_idx, local_idx=0, prior_leaves=1, parent=None):
        self.__parent = parent
        self.__tag = vals[0]
        self.__root_idx = root_idx
        self.__local_idx = local_idx

        children = vals[1:][0]

        if self.__tag== 'PRP$':
            assert (isinstance(children, str) or isinstance(children, unicode))
            self.__tag = 'NP'
            children = [[u'PRP', children],]

        if self.__tag == 'NP':
            Tree.NP_nodes.add(self)
        elif self.__tag == 'PRP':
            Tree.PR_nodes.add(parent)

        self.__config = None

        if isinstance(children, str) or isinstance(children, unicode):
            if self.__tag.startswith("PRP") and children not in Tree.lexicon:
                children = children.lower()
            self.__node = Head(children, prior_leaves)
            self.__leaf = True
            if self.__tag.startswith("N") or self.__tag.startswith("PR"):
                conf = Tree.lexicon.get(self.__node.get_string())
                if not conf:
                    conf = {"gender": "[fm]",
                            "person": "t",
                            "count": "s" if self.__tag == "NN" else "p",
                            "case": "obj|dat|nom",
                            "type": "R"
                        }

                    Tree.lexicon[self.__node.get_string()] = conf

                self.__config = conf
                self.__parent.set_config(conf)

        else:
            self.__node = Bar(children, root_idx, local_idx, prior_leaves, self)
            self.__leaf = False


    def num_leaves(self):
        return self.__node.num_leaves()

    def size_of_subtree(self):
        # if this is not true, may find duplicates later in the tree
        # need to build tree left to right to be consistent
        return self.__node.size_of_subtree()


    def __hash__(self):
        return hash((self.__root_idx, self.__local_idx))

    def tag(self):
        return self.__tag

    def parent(self):
        return self.__parent

    def is_leaf(self):
        return self.__leaf

    def pretty_print(self, depth=0):
        print(" " * depth + self.__tag + ":")
        self.__node.pretty_print(depth + 4)

    def get_string(self):
        return self.__node.get_string()

    def set_string(self, val):
        self.__node.set_string(val)

    def get_children(self):
        return self.__node.get_children()

    def set_config(self, config):
        assert (self.__tag.endswith("NP"))
        self.__config = config

    def config(self):
        return self.__config

    def min_leaf(self):
        return self.__node.min_leaf()

    def max_leaf(self):
        return self.__node.max_leaf()

    def leaf_range(self):
        return self.__node.min_leaf(), self.__node.max_leaf()

class Bar:
    disable_pruning = True

    def __init__(self, vals, root_idx, local_idx, prior_leaves, parent):
        self.__parent = parent

        c_index = local_idx + 1
        self.__min_leaf = prior_leaves
        self.__num_leaves = 0
        self.__children = []
        for x in vals:
            t = Tree(x, root_idx, c_index, prior_leaves + self.__num_leaves, parent)
            c_index += t.size_of_subtree()
            self.__num_leaves += t.num_leaves()
            self.__children.append(t)

        self.__size_of_subtree = c_index - local_idx

        if len(self.__children) < 1:
            print ("Bar must have at least one child")
            return

        for x in range(len(self.__children) - 1):
            # handles cases such as "each other"
            combo_str = self.__children[x].get_string() + " " + self.__children[x + 1].get_string()
            if combo_str in Tree.lexicon:
                assert (parent.tag() == "NP")
                conf = Tree.lexicon[combo_str]
                if conf["type"] != "R":
                    Tree.PR_nodes.add(parent)
                    assert (parent in Tree.NP_nodes)
                parent.set_config(conf)

        if Bar.disable_pruning:
            return

        # eliminates some non-binary branching, if needed
        check = find_pair(self.__children)
        while not (check == (-1, -1, -1)):
            e1, e2 = self.__children[check[0]], self.__children[check[0] + 1]
            self.__children[check[1]].set_string(e1.get_string() + " " + e2.get_string())
            self.__children.pop(check[2])
            check = find_pair(self.__children)

    def min_leaf(self):
        return self.__min_leaf

    def max_leaf(self):
        return self.__min_leaf + self.__num_leaves

    def size_of_subtree(self):
        return self.__size_of_subtree

    def num_leaves(self):
        return self.__num_leaves

    def pretty_print(self, depth=0):
        for x in self.__children:
            x.pretty_print(depth)

    def get_children(self):
        return self.__children

    def get_prev(self):
        return

    def get_next(self):
        return

    def get_string(self):
        retval = ""
        for elem in self.__children:
            if retval:
                retval += " "
            retval += elem.get_string()
        return retval

    def set_string(self, val):
        print ("WARNING: attempting to set string at bar level")

class Head:
    def __init__(self, val, leaf_index):
        self.__val = val
        self.__leaf_index = leaf_index

    def pretty_print(self, depth):
        print(" " * depth + self.__val)

    def get_string(self):
        return self.__val

    def get_children(self):
        return []

    def set_string(self, val):
        self.__val = val

    def size_of_subtree(self):
        return 1

    def num_leaves(self):
        return 1

    def min_leaf(self):
        return self.__leaf_index

    def max_leaf(self):
        return self.__leaf_index + 1


def is_leaf(val):
    return isinstance(val, Head)

def get_parent(val):
    return val.parent()

def get_index(word, sentence):
    if isinstance(sentence, Tree):
        words = sentence.get_string().split()
    else:
        words = sentence.split()
    index = 0
    for w in words:
        if word == w:
            return index
        index += 1
    return -1

def find_pair(treelist):
    prev_elem = treelist[0]
    for x in range(1, len(treelist)):
        elem = treelist[x]
        # first value is the start index, second is the one
        # we want to keep, third is the one we discard
        if prev_elem.tag() == 'MD' and elem.tag() == 'RB':
            return x - 1, x - 1, x
        if prev_elem.tag() == 'RB' and elem.tag() == 'JJ':
            return x - 1, x, x - 1

    return -1, -1, -1

WS = re.compile("\s")

def process_string(val):
    current_str = ""
    current_depth = 0
    completed_stack = []
    waiting_stack = []

    searching = False
    root = False
    for c in val:
        if c == "(":
            current_depth += 1
            waiting_stack.append([])

        elif c == ")":
            assert (not root)
            if current_str:
                waiting_stack[-1][1].append(current_str)
            if len(waiting_stack) > 1:
                tmp = waiting_stack[-1]
                waiting_stack.pop()
                if len(tmp[1]) == 1 and (isinstance(tmp[1][0], str) or
                                         isinstance(tmp[1][0], unicode)):
                    tmp[1] = tmp[1][0]
                waiting_stack[-1][1].append(tmp)

            current_str = ""

        elif WS.match(c):
            if current_str:
                if not waiting_stack[-1]:
                    waiting_stack[-1].append(current_str)
                    waiting_stack[-1].append([])
                else:
                    waiting_stack[-1][1].append(current_str)
                current_str = ""

        else:
            current_str += c
    return waiting_stack
