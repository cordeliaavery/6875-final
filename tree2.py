
class NodeError(Exception):
    def __init__(self, expression):
        self.expression = expression
        self.message = "Attempting to access child at leaf!"

class Tree:
    def __init__(self, vals, parent=None):
        self.__parent = parent
        self.__tag = vals[0]

        children = vals[1:][0]
        if isinstance(children, str) or isinstance(children, unicode):
            self.__node = Head(children, self)
            self.__leaf = True
        else:
            self.__node = Bar(children, self)
            self.__leaf = False

    def tag(self):
        return self.__tag

    def parent(self):
        return self.__parent

    def get_left(self):
        if isinstance(self.__node, Bar):
            return self.__node.get_left()
        raise NodeError

    def get_right(self):
        if isinstance(self.__node, Bar):
            return self.__node.get_right()
        raise NodeError

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

class Bar:
    def __init__(self, vals, parent):
        self.__parent = parent

        #self.__left = Tree(vals[0], parent)
        #if len(vals) > 1:
        #    self.__right = Tree(vals[1], parent)
        #else:
        #    self.__right = None

        self.__extras = []
        for x in vals:
            self.__extras.append(Tree(x, parent))

        if len(self.__extras) < 1:
            print ("Bar must have at least one child")
            return
        if len(self.__extras) == 1:
            self.__left = self.__extras[0]
            self.__right = None
            return
        if len(self.__extras) == 2:
            self.__left, self.__right = self.__extras
            return

        check = find_pair(self.__extras)
        while not (check == (-1, -1, -1)):
            e1, e2 = self.__extras[check[0]], self.__extras[check[0] + 1]
            self.__extras[check[1]].set_string(e1.get_string() + " " + e2.get_string())
            self.__extras.pop(check[2])
            check = find_pair(self.__extras)

        self.__left = self.__extras[0]
        if len(self.__extras) > 1:
            self.__right = self.__extras[1]
        else:
            self.__right = None


    def pretty_print(self, depth=0):
        for x in self.__extras:
            x.pretty_print(depth)
        return
        if self.__left:
            self.__left.pretty_print(depth)
        if self.__right:
            self.__right.pretty_print(depth)

    def get_children(self):
        return self.__extras

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right

    def set_left(self, left):
        self.__left = left

    def set_right(self, right):
        self.__right = right

    def get_prev(self):
        return

    def get_next(self):
        return

    def get_string(self):
        retval = ""
        for elem in self.__extras:
            if retval:
                retval += " "
            retval += elem.get_string()
        return retval

    def set_string(self, val):
        print ("WARNING: attempting to set string at bar level")

class Head:
    def __init__(self, val, parent):
        self.__val = val
        self.__parent = parent

    def pretty_print(self, depth):
        print(" " * depth + self.__val)

    def get_string(self):
        return self.__val

    def get_children(self):
        return []

    def set_string(self, val):
        self.__val = val

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
            print "comp md"
            return x - 1, x - 1, x
        if prev_elem.tag() == 'RB' and elem.tag() == 'JJ':
            print "comp rb"
            return x - 1, x, x - 1
        if prev_elem.tag() == 'JJ' and elem.tag().startswith('NN'):
            print "comp jj"
            return x - 1, x, x - 1
    return -1, -1, -1
