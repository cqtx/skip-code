# Usage Guide

Practical workflows for the Skip-Code toolkit beyond the quick examples in the
main README.

## Linear Skip-Code Runs

### Single Interval

```bash
python -m skip_code --text "THE QUICK BROWN FOX" --interval 7
```

- Filters to letters and uppercases by default (`THEQUICKBROWNFOX`).
- Displays the 7th, 14th, 21st, ... letters as a single sequence.

### Multiple Intervals

```bash
python -m skip_code --file sample.txt --interval 5 --interval 12
```

- You can combine explicit intervals. Each interval is reported separately.
- The order of `--interval` flags does not matter; output is sorted numerically.

### Automatic Interval Sweep

```bash
python -m skip_code --file sample.txt --auto-start 10 --auto-end 50 --auto-step 5
```

- Generates intervals `[10, 15, 20, 25, 30, 35, 40, 45, 50]`.
- Handy when you want to skim a range without specifying each value.

## Pattern-Based Searches

### Enabling Dictionary Lookups

```bash
python -m skip_code --file sample_grid.txt \
  --interval 8 \
  --dictionary data/words_alpha.txt \
  --directions N NE E SE S SW W NW
```

- Pattern search runs after the linear phase unless you add `--disable-patterns`.
- If no dictionary can be loaded, the tool warns and skips pattern output.

### Threshold Alerts

```bash
python -m skip_code --file sample_grid.txt \
  --interval 21 \
  --dictionary data/words_alpha.txt \
  --threshold 10
```

- Counts unique dictionary words found in the grid.
- Prints `"[Alert]"` when the threshold is met or exceeded.

### Limiting Directions and Disabling Reversed Words

```bash
python -m skip_code --file sample_grid.txt \
  --interval 30 \
  --dictionary data/words_alpha.txt \
  --directions N S \
  --no-reversed
```

- Searches only north/south directions.
- Skips reversed word detection for faster scanning.

## Working With Custom Dictionaries

1. Create a text file with one word per line (alphabetic characters recommended).
2. Save it locally; for example `data/my_dictionary.txt`.
3. Run the tool with `--dictionary data/my_dictionary.txt`.

Words are uppercased internally, so case differences in your file do not matter.

## Using the Library Programmatically

```python
from skip_code.linear import extract_skip_sequences
from skip_code.grid import TextGrid, find_words_in_grid
from skip_code.dictionary import WordDictionary

text = "HELLO WORLD"
result = extract_skip_sequences(text, [3])
print(result.interval_sequences[3])

grid = TextGrid.from_text(text)
dictionary = WordDictionary.from_words(["HEL", "OWL"])
print(find_words_in_grid(grid, dictionary))
```

- Every module is importable; the package follows a regular Python API layout.
- `LinearExtractionResult` offers `interval_sequences` and the helper
  `non_empty()`.
- `TextGrid` exposes dimensions (`height`, `width`) and helpers like
  `in_bounds()`.

## Batch Processing Tips

- Combine the CLI with shell utilities such as `find` or `xargs` to scan many
  files.
- Redirect output to a file if you need to analyze long interval sweeps:
  `python -m skip_code ... > results.txt`.
- For repeat runs, consider writing a small shell script with your favorite
  parameters.
