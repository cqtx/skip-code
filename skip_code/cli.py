"""Command-line interface for the skip-code toolkit."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Optional

from .dictionary import WordDictionary, load_default_dictionary
from .grid import DIRECTION_VECTORS, PatternMatch, TextGrid, find_words_in_grid
from .linear import LinearExtractionResult, auto_intervals, extract_skip_sequences


def _load_text(source_file: Optional[Path], inline_text: Optional[str]) -> str:
    if bool(source_file) == bool(inline_text):
        raise ValueError("Provide exactly one of --file or --text")
    if source_file:
        return source_file.read_text(encoding="utf-8", errors="ignore")
    assert inline_text is not None
    return inline_text


def _collect_intervals(args: argparse.Namespace) -> List[int]:
    intervals: List[int] = []
    intervals.extend(args.interval or [])
    if args.auto_start and args.auto_end:
        intervals.extend(auto_intervals(args.auto_start, args.auto_end, args.auto_step))
    if not intervals:
        raise ValueError("No intervals provided; use --interval or --auto-start/--auto-end")
    return sorted(set(intervals))


def _print_linear_results(result: LinearExtractionResult) -> None:
    print("Linear Skip-Code Results:")
    print(f"  Source length: {result.source_length}")
    print(f"  Filtered length: {result.filtered_length}")
    for interval, sequence in sorted(result.interval_sequences.items()):
        preview = sequence if sequence else "(empty)"
        print(f"  Interval {interval}: {preview}")
    print()


def _load_dictionary(args: argparse.Namespace) -> Optional[WordDictionary]:
    dictionary = load_default_dictionary(args.dictionary)
    if dictionary is None:
        print("[Warning] No dictionary available; pattern search skipped.")
    return dictionary


def _print_pattern_matches(matches: List[PatternMatch]) -> None:
    if not matches:
        print("Pattern Search: no matches found.")
        return

    print("Pattern Search Matches:")
    for match in matches:
        orientation = "reversed" if match.reversed else "forward"
        print(
            "  "
            f"{match.word} at (row={match.start_row}, col={match.start_col}) "
            f"dir={match.direction} [{orientation}]"
        )
    print(f"Total matches: {len(matches)}")
    print()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Skip-code extraction and pattern search tool")
    parser.add_argument("--file", type=Path, help="Path to input text file")
    parser.add_argument("--text", help="Inline text to analyze")
    parser.add_argument(
        "--interval",
        type=int,
        action="append",
        help="Explicit interval to evaluate; can be repeated",
    )
    parser.add_argument("--auto-start", type=int, help="Start of automatic interval range")
    parser.add_argument("--auto-end", type=int, help="End of automatic interval range")
    parser.add_argument("--auto-step", type=int, default=1, help="Step size for automatic range")
    parser.add_argument(
        "--keep-nonletters",
        action="store_false",
        dest="letters_only",
        default=True,
        help="Retain non-letter characters instead of filtering them",
    )
    parser.add_argument(
        "--keep-case",
        action="store_true",
        default=False,
        help="Preserve original character case (default uppercases)",
    )
    parser.add_argument("--dictionary", type=str, help="Path to dictionary file to validate words")
    parser.add_argument(
        "--disable-patterns",
        action="store_true",
        help="Skip diagonal/pattern-based searches",
    )
    parser.add_argument("--min-word-length", type=int, default=3, help="Minimum word length to report")
    parser.add_argument(
        "--max-word-length",
        type=int,
        help="Maximum word length to consider (defaults to dictionary maximum)",
    )
    parser.add_argument(
        "--directions",
        nargs="+",
        choices=sorted(DIRECTION_VECTORS.keys()),
        help="Subset of directions to evaluate",
    )
    parser.add_argument(
        "--no-reversed",
        action="store_true",
        help="Disable detection of reversed words",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=0,
        help="Alert threshold for number of dictionary words discovered",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        text = _load_text(args.file, args.text)
        intervals = _collect_intervals(args)
    except ValueError as exc:
        parser.error(str(exc))
        return

    linear_result = extract_skip_sequences(
        text,
        intervals,
        letters_only=args.letters_only,
        uppercase=not args.keep_case,
    )
    _print_linear_results(linear_result)

    if args.disable_patterns:
        return

    dictionary = _load_dictionary(args)
    if dictionary is None:
        return

    grid = TextGrid.from_text(
        text,
        letters_only=args.letters_only,
        uppercase=not args.keep_case,
    )

    matches = find_words_in_grid(
        grid,
        dictionary,
        min_length=args.min_word_length,
        max_length=args.max_word_length,
        directions=args.directions,
        include_reversed=not args.no_reversed,
    )
    _print_pattern_matches(matches)

    if args.threshold > 0:
        unique_words = {match.word for match in matches}
        if len(unique_words) >= args.threshold:
            print(
                f"[Alert] Threshold met: {len(unique_words)} unique words (threshold={args.threshold})."
            )
        else:
            print(
                f"Words discovered: {len(unique_words)} (threshold={args.threshold})."
            )


if __name__ == "__main__":
    main()
