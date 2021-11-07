import random
from dataclasses import dataclass
from typing import List

from core.graph import Graph, Node, State
from lex.neo4j.phrase_dao import PhraseDao
from puzzle.elements import Word, Dir, Puzzle, BLANK


@dataclass
class Change:
    word: Word
    value: str


def get_completions_for(word: Word, puzzle: Puzzle):
    # todo caching, and signal a dead-end word. That is,
    #   a word for which all possible changes are dead-ended.
    current = puzzle.string_from(word)
    dao = PhraseDao()
    return dao.match(current)


def choose_next_change(words: List[Word], puzzle: Puzzle) -> Change:
    word_to_change = random.choice(words)
    possible_completions = get_completions_for(word_to_change, puzzle)
    return random.choice(possible_completions)  # todo scoring, exclude dead ends


def construct():
    #  T-shaped puzzle of two 3-letter words
    #  [0][1][2]
    #     [3]
    #     [4]
    acr_1 = Word(1, Dir.ACROSS, [0, 1, 2])
    dn_2 = Word(2, Dir.DOWN, [1, 3, 4])

    initial_grid: List[chr] = list(BLANK * 8)

    puz = Puzzle(initial_grid, [acr_1, dn_2])

    cursor = Graph(Node(puz)).get_cursor()

    while not puz.complete():
        incompletes = puz.get_incomplete_words()
        change = choose_next_change(incompletes, puz)
        if change is not None:
            idx = 0  # todo need to map Word -> idx, or change mutate's signature
            new_puz = puz.mutate(idx, change.value)
        else:
            cursor.backtrack()
            cursor.set_child_state(change, State.DEAD_END)
            puz = cursor.node.data


if __name__ == '__main__':
    construct()
