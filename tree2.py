
class NodeError(Exception):
    def __init__(self, expression):
        self.expression = expression
        self.message = "Attempting to access child at leaf!"

class Tree:
    def __init__(self, vals, parent=None):
        self.__parent = parent
        if len(vals) != 2:
            print ("VALS dict must contain a single item")
            exit
        (self.__tag, children) = vals
        if isinstance(children, str):
            self.__node = Head(children, self)
        else:
            self.__node = Bar(children, self)

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

    def pretty_print(self, depth=0):
        print(" " * depth + self.__tag)
        self.__node.pretty_print(depth + 4)

class Bar:
    def __init__(self, vals, parent):
        self.__parent = parent
        if not vals or len(vals) > 2:
            print ("VALS must have 1 or 2 items")
            exit
        self.__left = Tree(vals[0], parent)
        if len(vals) > 1:
            self.__right = Tree(vals[1], parent)
        else:
            self.__right = None

    def pretty_print(self, depth=0):
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

class Head:
    def __init__(self, val, parent):
        self.__val = val
        self.__parent = parent

    def pretty_print(self, depth):
        print(" " * depth + self.__val)

def is_leaf(val):
    return isinstance(val, Head)

def get_parent(val):
    return val.parent()
