# API Reference

This document summarizes the public interfaces exposed by the Skip-Code package.

## Module: `skip_code.linear`

### `extract_skip_sequences(text, intervals, *, letters_only=True, uppercase=True)`

- Returns a `LinearExtractionResult` with:
  - `interval_sequences`: mapping of interval → extracted string.
  - `source_length`: original length of `text`.
  - `filtered_length`: length after optional filtering or normalization.
- Skips non-positive intervals.
- When `letters_only=True`, only alphabetic characters are kept (`str.isalpha()`).
- When `uppercase=True`, remaining characters are uppercased.

### `LinearExtractionResult`

Attributes:

- `interval_sequences`
- `source_length`
- `filtered_length`

Methods:

- `non_empty()` → dictionary limited to intervals that produced non-empty strings.

### `auto_intervals(start, end, step=1)`

- Convenience helper that returns `[start, start + step, …, end]`.
- Raises `ValueError` if any arguments are non-positive or if `end < start`.

## Module: `skip_code.grid`

### `TextGrid.from_text(text, *, letters_only=True, uppercase=True)`

- Splits `text` into rows via `splitlines()`.
- Filters non-letters and applies uppercase by default.
- Returns a `TextGrid` instance containing a list of rows.

### `TextGrid`

Properties and methods:

- `rows`: list of list of characters.
- `height`, `width`: grid dimensions.
- `in_bounds(row, col)`: check coordinate validity.
- `iter_start_positions()`: generator over every valid `(row, col)` start.
- `char_at(row, col)`: safe character lookup or `None` if out of bounds.

### `find_words_in_grid(...)`

- Signature: `(grid, dictionary, *, min_length=3, max_length=None,
  directions=None, include_reversed=True)`.
- Iterates over provided `directions`
  (`['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']`).
- Stops extending a path if no dictionary prefix matches, improving performance.
- Returns a list of `PatternMatch` instances, each with fields:
  - `word`
  - `start_row`, `start_col`
  - `direction`
  - `reversed`

### `PatternMatch`

- Data class describing a single successful match.
- When `reversed=True`, `start_row` and `start_col` point to the position where
  the reversed word begins (the final letter in the forward direction).

## Module: `skip_code.dictionary`

### `WordDictionary.from_words(iterable)`

- Normalizes input words to uppercase and trims whitespace.
- Builds a prefix cache to support fast pruning during grid traversal.

### `WordDictionary.from_file(path)`

- Reads newline-separated words from disk.

### `WordDictionary.contains(word)` / `has_prefix(prefix)`

- Simple membership tests against the internal sets.

### `load_default_dictionary(explicit_path=None)`

- Tries `explicit_path` first; otherwise checks `/usr/share/dict/words` and
  `/usr/dict/words`.
- Returns a `WordDictionary` or `None` if no file can be read.

## Module: `skip_code.cli`

### `main(argv=None)`

- Entry point for the command-line interface. In practice you will invoke it via
  `python -m skip_code ...`.
- Handles argument parsing, linear extraction, optional pattern search, and
  threshold alerts.

### Key Helpers

- `_load_text(source_file, inline_text)` ensures mutually exclusive choice
  between `--file` and `--text`.
- `_collect_intervals(args)` combines explicit intervals with auto-generated
  ranges.
- `_load_dictionary(args)` wires the dictionary loader and prints a warning if
  nothing can be loaded.

## Command-Line Arguments (quick reminder)

- Documented in detail in `README.md` and `docs/usage.md`.
- The CLI returns exit code 0 on success; validation errors (missing intervals or
  absent input) surface via argparse and exit with non-zero status.
