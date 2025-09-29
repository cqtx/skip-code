# Example Scenarios

Small, self-contained walkthroughs that pair input files with commands and
highlight what to look for.

## 1. Triple-Word Mini Crossword

- Dictionary: `data/demo_dictionary1.txt`
- Grid: `data/demo_text1.txt`
- Command:

  ```bash
  python -m skip_code --file data/demo_text1.txt \
    --interval 2 \
    --dictionary data/demo_dictionary1.txt \
    --directions E S \
    --min-word-length 3 \
    --max-word-length 3 \
    --no-reversed
  ```

Key takeaways:

- Revisits the README example but reinforces how east/south only searches behave.
- Linear interval 2 highlights how alternating characters form the acrostic
  `AAOO`.

## 2. Diagonal Word Hunt

- Text:

  ```text
  MAGE
  ARIA
  GALA
  EARS
  ```

- Dictionary inline:

  ```text
  MAGA
  MARS
  AGES
  RIA
  ```

- Command (inline inputs shown via shell here-documents):

  ```bash
  python -m skip_code --text $'MAGE\nARIA\nGALA\nEARS' \
    --interval 4 \
    --dictionary data/words_alpha.txt \
    --directions NE SE \
    --min-word-length 4
  ```

Highlights:

- Demonstrates searching only diagonal directions.
- Useful when you expect diagonals to encode messages while rows/columns are
  noise.

## 3. Reversed Word Alert

- Text:

  ```text
  LEVEL
  LEVEL
  LEVEL
  ```

- Dictionary inline:

  ```text
  LEVEL
  LEV
  ```

- Command:

  ```bash
  python -m skip_code --text $'LEVEL\nLEVEL\nLEVEL' \
    --interval 5 \
    --dictionary data/words_alpha.txt \
    --threshold 2
  ```

Highlights:

- Shows how palindromes appear twice in the pattern output: forward and
  reversed.
- Threshold alert fires when both unique words are found.

Feel free to drop additional Markdown files in this directory for new
experiments.
