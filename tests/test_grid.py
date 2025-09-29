from skip_code.dictionary import WordDictionary
from skip_code.grid import TextGrid, find_words_in_grid


def test_find_words_in_grid_basic():
    text = "CAT\nAGO\nTOP"
    grid = TextGrid.from_text(text)
    dictionary = WordDictionary.from_words(["CAT", "AGO", "TOP"])

    matches = find_words_in_grid(grid, dictionary, include_reversed=False)

    observed = {(m.word, m.start_row, m.start_col, m.direction) for m in matches}
    expected = {
        ("CAT", 0, 0, "E"),
        ("CAT", 0, 0, "S"),
        ("AGO", 1, 0, "E"),
        ("AGO", 0, 1, "S"),
        ("TOP", 2, 0, "E"),
        ("TOP", 0, 2, "S"),
    }

    assert expected.issubset(observed)


def test_find_words_in_grid_detects_reversed_words():
    text = "CAT"
    grid = TextGrid.from_text(text)
    dictionary = WordDictionary.from_words(["CAT", "TAC"])

    matches = find_words_in_grid(grid, dictionary, include_reversed=True)

    summary = {(m.word, m.direction, m.reversed) for m in matches}
    assert ("CAT", "E", False) in summary
    assert ("TAC", "W", True) in summary


def test_find_words_in_grid_diagonal_subset():
    text = "ABC\nDEF\nGHI"
    grid = TextGrid.from_text(text)
    dictionary = WordDictionary.from_words(["AEI", "ADG", "CFI"])

    matches = find_words_in_grid(
        grid,
        dictionary,
        directions=["SE"],
        include_reversed=False,
    )

    found = {(m.word, m.direction) for m in matches}
    assert ("AEI", "SE") in found
    assert all(direction == "SE" for _, direction in found)
