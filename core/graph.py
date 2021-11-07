from enum import Enum

from construct.construct import Change


class State(Enum):
    DEAD_END = -1
    UNEXPLORED = 0


class Node:
    edges = {}

    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent

    def add_child_node(self, change: Change, node):
        self.edges[change] = node

    def add_child_unexplored(self, change: Change):
        self.edges[change] = State.UNEXPLORED

    def set_child_node(self, change: Change, node):
        self.edges[change] = node

    def set_child_state(self, change: Change, state: State):
        self.edges[change] = state


class Graph:
    def __init__(self, root: Node):
        self.root = root

    def get_cursor(self):
        return Cursor(self.root)


class Cursor:
    def __init__(self, node: Node):
        self.node = node

    def backtrack(self) -> bool:
        if self.node.parent is not None:
            self.node = self.node.parent
            return True
        else:
            return False

    def add_child_node(self, change: Change, node):
        self.node.add_child_node(change, node)

    def add_child_state(self, change: Change):
        self.node.add_child_unexplored(change)

    def set_child_node(self, change: Change, node):
        self.node.set_child_node(change, node)

    def set_child_state(self, change: Change, state: State):
        self.node.set_child_state(change, state)
