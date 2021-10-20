from dataclasses import dataclass
from enum import Enum
from typing import List

BLANK = '_'


class Dir(Enum):
    #  Note: values determine the sort order
    ACROSS = 0
    DOWN = 1


@dataclass
class Word:
    number: int
    direction: Dir
    grid_indices: List[int]
    blanks: int = 0

    def __len__(self):
        return len(self.grid_indices)

    def sort_key(self):
        return f'{self.direction.value} {self.number}'


class Puzzle:

    def __init__(self, initial_grid: List[chr], words: List[Word]):
        self.grid = initial_grid.copy()
        self.words = words.copy()
        self.init_grid()

    def init_grid(self):
        for w in self.words:
            blanks = 0
            for idx in w.grid_indices:
                if idx < 0 or idx >= len(self.grid):
                    raise IndexError(f'Word contains invalid index {idx}')
                if self.grid[idx] == BLANK:
                    blanks += 1
            w.blanks = blanks

    #  Override the [] accessors
    def __getitem__(self, idx):
        return self.grid[idx]

    def get_word(self, idx):
        return self.__string_from(self.words[idx])

    def get_incomplete_words(self):
        incompletes = [w for w in self.words if self.__incomplete(w)]
        return sorted(incompletes, key=lambda w: w.blanks, reverse=True)

    # def remaining_blanks(self, word: Word):
    #     return reduce(lambda i, _: i+1 if self.grid[i] == BLANK else i, word.grid_indices)

    def __incomplete(self, word: Word):
        for i in word.grid_indices:
            if self.grid[i] == BLANK:
                return True
        return False

    def __string_from(self, word):
        result = ''
        for idx in word.grid_indices:
            result += self.grid[idx]
        return result

    def mutate(self, idx, value):
        word = self.words[idx]
        if len(word) != len(value):
            raise ValueError(f'Word supplied (length {len(value)}) does not match target (length {len(word)}).')
        grid_copy = self.grid.copy()
        for idx, c in enumerate(value):
            grid_idx = word.grid_indices[idx]
            grid_copy[grid_idx] = c
        return Puzzle(grid_copy, self.words)

    def __str__(self):
        result = ''
        words_sorted = sorted(self.words, key=lambda word: word.sort_key())
        for w in words_sorted:
            result += f'{w.number} {w.direction.name} {self.__string_from(w)}\n'
        return result
