from typing import List

from puzzle.elements import Word, Dir, Puzzle, BLANK


def construct():
    #  T-shaped puzzle of two 3-letter words
    #  [0][1][2]
    #     [3]
    #     [4]
    acr_1 = Word(1, Dir.ACROSS, [0, 1, 2])
    dn_2 = Word(2, Dir.DOWN, [1, 3, 4])

    initial_grid: List[chr] = list(BLANK * 8)

    puz = Puzzle(initial_grid, [acr_1, dn_2])

    print(str(puz))


if __name__ == '__main__':
    construct()
