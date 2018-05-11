import re

WS = re.compile("\s")

def process_string(val):
    current_str = ""
    current_depth = 0
    completed_stack = []
    waiting_stack = [] #[[]]

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

class NodeError(Exception):
    def __init__(self, expression):
        self.expression = expression
        self.message = "Attempting to access child at leaf!"

class Tree:
    def __init__(self, vals_str, parent=None):
        self.__parent = parent
        vals_str = vals_str.strip()
        if not vals_str[0] == "(" or not vals_str[-1] == ")":
            raise ValueError
        self.__tag = vals_str[1:-1].strip().split()[0]
        vals = vals_str[len(self.__tag) + 1:-1].strip()
            
        if len(vals) != 2:
            print ("VALS dict must contain a single item")
            exit

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
