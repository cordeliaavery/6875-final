
class Tree:
    def __init__(self, vals, parent=None):
        if len(vals) != 1:
            print ("VALS dict must contain a single item")
            exit
        (self.__tag, children) = vals.items()[0]
        if isinstance(children, str):
            self.__node = Head(children, self)
        else:
            self.__node = Bar(children, self)

    def get_tag(self):
        return self.__tag

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
