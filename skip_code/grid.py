"""Grid utilities for pattern-based searches (Phase 2)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple

from .dictionary import WordDictionary


Direction = Tuple[int, int]
DIRECTION_VECTORS = {
    "N": (-1, 0),
    "NE": (-1, 1),
    "E": (0, 1),
    "SE": (1, 1),
    "S": (1, 0),
    "SW": (1, -1),
    "W": (0, -1),
    "NW": (-1, -1),
}

OPPOSITE_DIRECTIONS = {
    "N": "S",
    "NE": "SW",
    "E": "W",
    "SE": "NW",
    "S": "N",
    "SW": "NE",
    "W": "E",
    "NW": "SE",
}


@dataclass
class PatternMatch:
    word: str
    start_row: int
    start_col: int
    direction: str
    reversed: bool = False


@dataclass
class TextGrid:
    rows: List[List[str]]

    @classmethod
    def from_text(
        cls,
        text: str,
        *,
        letters_only: bool = True,
        uppercase: bool = True,
    ) -> "TextGrid":
        rows: List[List[str]] = []
        for raw_line in text.splitlines():
            row: List[str] = []
            for ch in raw_line:
                if letters_only and not ch.isalpha():
                    continue
                row.append(ch.upper() if uppercase else ch)
            if row:
                rows.append(row)
        return cls(rows=rows)

    @property
    def height(self) -> int:
        return len(self.rows)

    @property
    def width(self) -> int:
        return max((len(row) for row in self.rows), default=0)

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.height and 0 <= col < len(self.rows[row])

    def iter_start_positions(self) -> Iterable[Tuple[int, int]]:
        for r, row in enumerate(self.rows):
            for c in range(len(row)):
                yield r, c

    def char_at(self, row: int, col: int) -> Optional[str]:
        if self.in_bounds(row, col):
            return self.rows[row][col]
        return None


def find_words_in_grid(
    grid: TextGrid,
    dictionary: WordDictionary,
    *,
    min_length: int = 3,
    max_length: Optional[int] = None,
    directions: Optional[Sequence[str]] = None,
    include_reversed: bool = True,
) -> List[PatternMatch]:
    """Scan *grid* for dictionary words in the provided *directions*."""

    if grid.height == 0:
        return []

    allowed_dirs = directions or list(DIRECTION_VECTORS.keys())
    vectors = [(name, DIRECTION_VECTORS[name]) for name in allowed_dirs if name in DIRECTION_VECTORS]

    if not vectors:
        return []

    max_len = max_length or dictionary.max_length
    matches: List[PatternMatch] = []
    seen = set()

    for start_row, start_col in grid.iter_start_positions():
        for direction_name, (dr, dc) in vectors:
            letters: List[str] = []
            row, col = start_row, start_col
            while grid.in_bounds(row, col):
                letters.append(grid.rows[row][col])
                current = "".join(letters)
                if len(current) > max_len:
                    break
                if len(current) >= min_length and dictionary.contains(current):
                    key = (current, start_row, start_col, direction_name, False)
                    if key not in seen:
                        seen.add(key)
                        matches.append(
                            PatternMatch(
                                word=current,
                                start_row=start_row,
                                start_col=start_col,
                                direction=direction_name,
                                reversed=False,
                            )
                        )
                if include_reversed and len(current) >= min_length:
                    reversed_word = current[::-1]
                    if dictionary.contains(reversed_word):
                        start_r, start_c = row, col
                        direction_out = OPPOSITE_DIRECTIONS.get(direction_name, direction_name)
                        key = (reversed_word, start_r, start_c, direction_out, True)
                        if key not in seen:
                            seen.add(key)
                            matches.append(
                                PatternMatch(
                                    word=reversed_word,
                                    start_row=start_r,
                                    start_col=start_c,
                                    direction=direction_out,
                                    reversed=True,
                                )
                            )
                if not (
                    dictionary.has_prefix(current)
                    or (include_reversed and dictionary.has_prefix(current[::-1]))
                ):
                    break
                row += dr
                col += dc
    return matches
