
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

class Bar:
    def __init__(self, vals, parent):
        self.__parent = parent

        self.__left = Tree(vals[0], parent)
        if len(vals) > 1:
            self.__right = Tree(vals[1], parent)
        else:
            self.__right = None

        self.__extras = []
        for x in vals:
            self.__extras.append(Tree(x, parent))

    def pretty_print(self, depth=0):
        for x in self.__extras:
            x.pretty_print(depth)
        return
        if self.__left:
            self.__left.pretty_print(depth)
        if self.__right:
            self.__right.pretty_print(depth)

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


class Head:
    def __init__(self, val, parent):
        self.__val = val
        self.__parent = parent

    def pretty_print(self, depth):
        print(" " * depth + self.__val)

    def get_string(self):
        return self.__val

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
