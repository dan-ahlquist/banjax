from enum import Enum

from puzzle.elements import Word


class State(Enum):
    DEAD_END = -1
    UNEXPLORED = 0


class Node:
    edges = {}

    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent

    def add_child_node(self, change: Word, node):
        self.edges[change] = node

    def add_child_state(self, change: Word):
        self.edges[change] = State.UNEXPLORED

    def set_child_node(self, change: Word, node):
        self.edges[change] = node

    def set_child_state(self, change: Word, state: State):
        self.edges[change] = state


class Graph:
    def __init__(self, root: Node):
        self.root = root


class Cursor:
    def __init__(self, node: Node):
        self.node = node

    def backtrack(self) -> bool:
        if self.node.parent is not None:
            self.node = self.node.parent
            return True
        else:
            return False
