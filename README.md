# Skip-Code Toolkit

Command-line utility for extracting linear skip-code sequences and discovering
dictionary-backed word patterns in text grids. Written in Python and designed
for quick local experiments.

## Quick Start

```bash
python -m skip_code --file path/to/text.txt --interval 10 --auto-start 5 \
  --auto-end 25 --auto-step 5
```

- Reads either `--file` or `--text` (exactly one).
- Filters to letters and uppercases by default. Add `--keep-nonletters` or
  `--keep-case` to change that.
- Prints a line for each interval. Add `--disable-patterns` if you only care
  about the MVP linear output.

## CLI Reference

- `--file PATH` Read text from PATH (mutually exclusive with `--text`).
- `--text STRING` Provide inline text (mutually exclusive with `--file`). Use
  `$'line1\nline2'` to embed newlines in bash.
- `--interval N` Check interval N. Repeat the flag for multiple explicit
  intervals.
- `--auto-start A`, `--auto-end B`, `--auto-step S` Generate interval range from
  A to B inclusive stepping by S (default 1). Combine with explicit
  `--interval` values as needed.
- `--keep-nonletters` Preserve punctuation, digits, and whitespace instead of
  filtering to alphabetic characters.
- `--keep-case` Preserve the original case (default uppercases everything for
  easier matching).
- `--dictionary PATH` Use PATH as the dictionary. Falls back to
  `/usr/share/dict/words` and `/usr/dict/words` if not supplied.
- `--disable-patterns` Skip Phase 2 grid scanning and only print linear
  results.
- `--min-word-length N` Ignore pattern matches shorter than N (default 3).
- `--max-word-length N` Do not search beyond N characters (defaults to
  dictionary maximum).
- `--directions ...` Limit pattern search directions to the provided subset of
  `N NE E SE S SW W NW`.
- `--no-reversed` Disable reversed-word detection in the grid search.
- `--threshold K` Print an alert when at least K unique dictionary words are
  discovered.

## Tiny Examples

### Linear skip-code only

```bash
python -m skip_code --text "THE QUICK BROWN FOX" --interval 3 --disable-patterns
```

Output:

```text
Linear Skip-Code Results:
  Source length: 19
  Filtered length: 16
  Interval 3: EIBWO
```

### Pattern search on a 3x3 grid

Dictionary (save as `data/demo_dictionary1.txt`):

```text
CAT
AGO
TOP
```

(Sample files `data/demo_dictionary1.txt` and
`data/demo_text1.txt` are included for convenience.)

Text grid (save as `data/demo_text1.txt`):

```text
CAT
AGO
TOP
```

Command:

```bash
python -m skip_code --file data/demo_text1.txt \
  --interval 2 \
  --dictionary data/demo_dictionary1.txt \
  --directions E S \
  --min-word-length 3 \
  --max-word-length 3 \
  --no-reversed
```

Sample output:

```text
Linear Skip-Code Results:
  Source length: 11
  Filtered length: 9
  Interval 2: AAOO

Pattern Search Matches:
  CAT at (row=0, col=0) dir=E [forward]
  CAT at (row=0, col=0) dir=S [forward]
  AGO at (row=0, col=1) dir=S [forward]
  TOP at (row=0, col=2) dir=S [forward]
  AGO at (row=1, col=0) dir=E [forward]
  TOP at (row=2, col=0) dir=E [forward]
Total matches: 6
```

- The linear output takes every second character after filtering (`C A T A G O
  T O P` → positions 2, 4, 6, 8) which yields `AAOO`.
- Grid matches report each dictionary word, its starting coordinates, the
  direction of travel, and whether it was found forward or reversed. In this
  example every word appears horizontally and vertically in the tiny crossword,
  so you see six hits.

### Pattern search on a 4x4 grid

Dictionary (save as `data/demo_dictionary2.txt`):

```text
SINK
IRON
NODE
KNEE
SIN
INK
ONE
RINK
DONE
KENO
SNIP
NEON
```

Text grid (save as `data/demo_text2.txt`):

```text
SINK
IRON
NODE
KNEE
```

(Sample files `data/demo_dictionary2.txt` and
`data/demo_text2.txt` are included for convenience.)

Command:

```bash
python -m skip_code --file data/demo_text2.txt \
  --interval 3 \
  --dictionary data/demo_dictionary2.txt \
  --directions E S \
  --min-word-length 3 \
  --max-word-length 4 \
  --no-reversed
```

Sample output:

```text
Linear Skip-Code Results:
  Source length: 20
  Filtered length: 16
  Interval 3: NRNEE

Pattern Search Matches:
  SIN at (row=0, col=0) dir=E [forward]
  SINK at (row=0, col=0) dir=E [forward]
  SIN at (row=0, col=0) dir=S [forward]
  SINK at (row=0, col=0) dir=S [forward]
  INK at (row=0, col=1) dir=E [forward]
  IRON at (row=0, col=1) dir=S [forward]
  NODE at (row=0, col=2) dir=S [forward]
  KNEE at (row=0, col=3) dir=S [forward]
  IRON at (row=1, col=0) dir=E [forward]
  INK at (row=1, col=0) dir=S [forward]
  NODE at (row=2, col=0) dir=E [forward]
  KNEE at (row=3, col=0) dir=E [forward]
Total matches: 12
```

- The linear extraction samples every third character from `SINKIRONNODEKNEE`,
  producing `NRNEE`.
- With directions limited to east and south, the grid finder reports each word
  where it appears horizontally and vertically. Unused dictionary entries (for
  example, `RINK`) naturally stay absent.

## Testing

```bash
python -m pytest
```

Run the command from the project root. If `pytest` is not already installed, add
it with `python -m pip install pytest` (you can do this inside a virtual
environment). The suite currently covers both interval extraction and grid-based
discovery.
