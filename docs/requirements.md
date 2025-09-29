# Program Specification: Skip-Code and Pattern-Finding Tool

## Phase 1 (MVP): Linear Skip-Code Extraction

**Objective:** Create a program that scans a given text and extracts letters at
specified intervals to find hidden messages.

**Requirements:**

- Input: A text file or string containing the text to analyze.
- Configuration: A parameter to set the interval (e.g., every 10th letter,
  every 20th letter, and so forth).
- Automation: Ability to loop through multiple intervals automatically (for
  example, from every 10 letters up to every 1000 letters) and extract possible
  messages.
- Output: A list of extracted letter sequences for each interval checked.

## Phase 2: Diagonal and Pattern-Based Search

**Objective:** Extend the program to find hidden words in a grid-like pattern,
including diagonal or other crossword-style directions.

**Requirements:**

- Input: Same text input as Phase 1, but treated as a 2D grid if possible (e.g.,
  line by line).
- Pattern Search: Additional logic to check for words diagonally or in other
  directions across the grid.
- Dictionary Check: Integrate a dictionary file to verify if the extracted
  sequences form real words.
- Thresholds and Alerts: Option to configure a threshold for how many real
  words need to be found before the program flags a potential hidden message.
- Output: A summary of discovered words and their positions, both linear and
  diagonal.

---

And that should give you a solid starting point! We can always adjust or add
more detail as you go along.
