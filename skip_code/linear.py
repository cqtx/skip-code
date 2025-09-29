"""Utilities for extracting linear skip-code sequences."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass
class LinearExtractionResult:
    """Stores the extracted sequences for each interval."""

    interval_sequences: Dict[int, str]
    source_length: int
    filtered_length: int

    def non_empty(self) -> Dict[int, str]:
        """Return only the intervals that produced non-empty sequences."""

        return {k: v for k, v in self.interval_sequences.items() if v}


def _prepare_text(text: str, letters_only: bool, uppercase: bool) -> str:
    filtered_chars: List[str] = []
    for ch in text:
        if letters_only and not ch.isalpha():
            continue
        filtered_chars.append(ch.upper() if uppercase else ch)
    return "".join(filtered_chars)


def extract_skip_sequences(
    text: str,
    intervals: Iterable[int],
    *,
    letters_only: bool = True,
    uppercase: bool = True,
) -> LinearExtractionResult:
    """Extract characters from *text* at the provided *intervals*.

    Args:
        text: Input text to scan.
        intervals: Iterable of interval sizes (e.g., 10 for every 10th character).
        letters_only: When ``True`` (default) keeps alphabetic characters only.
        uppercase: When ``True`` (default) normalizes characters to uppercase.

    Returns:
        LinearExtractionResult containing sequences for each interval.
    """

    filtered = _prepare_text(text, letters_only=letters_only, uppercase=uppercase)
    sequences: Dict[int, str] = {}

    for interval in sorted(set(i for i in intervals if i > 0)):
        selection = [filtered[idx] for idx in range(interval - 1, len(filtered), interval)]
        sequences[interval] = "".join(selection)

    return LinearExtractionResult(
        interval_sequences=sequences,
        source_length=len(text),
        filtered_length=len(filtered),
    )


def auto_intervals(start: int, end: int, step: int = 1) -> List[int]:
    """Generate a list of intervals between *start* and *end* inclusive."""

    if start <= 0 or end <= 0:
        raise ValueError("interval bounds must be positive integers")
    if end < start:
        raise ValueError("end must be greater than or equal to start")
    if step <= 0:
        raise ValueError("step must be positive")
    return list(range(start, end + 1, step))
