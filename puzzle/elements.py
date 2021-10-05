from dataclasses import dataclass
from enum import Enum
from typing import List

BLANK: chr = '_'


class Dir(Enum):
    #  Note that values determine he sort order
    ACROSS = 0
    DOWN = 1


@dataclass
class Word:
    number: int
    direction: Dir
    grid_indices: List[int]

    def __len__(self):
        return len(self.grid_indices)

    def sort_key(self):
        return f'{self.direction.value} {self.number}'


class Puzzle:

    def __init__(self, initial_grid: List[chr], words: List[Word]):
        self.grid = initial_grid.copy()
        self.words = words.copy()
        self.validate_grid()

    def validate_grid(self):
        for w in self.words:
            for idx in w.grid_indices:
                if idx < 0 or idx >= len(self.grid):
                    raise IndexError(f'Word contains invalid index {idx}')

    #  Override the [] accessors
    def __getitem__(self, idx):
        return self.grid[idx]

    def __setitem__(self, idx, value):
        self.grid[idx] = value

    def get_word(self, idx):
        return self.__string_from(self.words[idx])

    def __string_from(self, word):
        result = ''
        for idx in word.grid_indices:
            result += self.grid[idx]
        return result

    def set_word(self, idx, value):
        word = self.words[idx]
        if len(word) != len(value):
            raise ValueError(f'Word supplied (length {len(value)}) does not match target (length {len(word)}).')
        for idx, c in enumerate(value):
            grid_idx = word.grid_indices[idx]
            self.grid[grid_idx] = c

    def __str__(self):
        result = ''
        words_sorted = sorted(self.words, key=lambda word: word.sort_key())
        for w in words_sorted:
            result += f'{w.number} {w.direction.name} {self.__string_from(w)}\n'
        return result
