"""Dictionary utilities for validating discovered word patterns."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Set


@dataclass
class WordDictionary:
    """In-memory dictionary supporting fast word and prefix lookups."""

    words: Set[str]
    prefixes: Set[str]
    max_length: int

    def contains(self, word: str) -> bool:
        return word in self.words

    def has_prefix(self, prefix: str) -> bool:
        return prefix in self.prefixes

    @classmethod
    def from_words(cls, words: Iterable[str]) -> "WordDictionary":
        normalized = {w.strip().upper() for w in words if w.strip()}
        prefixes: Set[str] = set()
        max_length = 0
        for word in normalized:
            max_length = max(max_length, len(word))
            for idx in range(1, len(word) + 1):
                prefixes.add(word[:idx])
        return cls(words=normalized, prefixes=prefixes, max_length=max_length)

    @classmethod
    def from_file(cls, path: Path) -> "WordDictionary":
        data = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        return cls.from_words(data)


def load_default_dictionary(explicit_path: Optional[str] = None) -> Optional[WordDictionary]:
    """Attempt to load a dictionary, trying the explicit path first."""

    candidate_paths = []
    if explicit_path:
        candidate_paths.append(Path(explicit_path))
    candidate_paths.extend(
        [
            Path("/usr/share/dict/words"),
            Path("/usr/dict/words"),
        ]
    )

    for path in candidate_paths:
        if path.is_file():
            try:
                return WordDictionary.from_file(path)
            except OSError:
                continue
    return None
