from skip_code.linear import extract_skip_sequences


def test_extract_skip_sequences_basic():
    text = "THE QUICK BROWN FOX"
    result = extract_skip_sequences(text, [3], letters_only=True)
    assert result.filtered_length == 16  # spaces removed
    assert result.interval_sequences[3] == "EIBWO"


def test_extract_skip_sequences_with_nonletters():
    text = "A1B2C3D4E5"
    result = extract_skip_sequences(text, [2], letters_only=False)

    assert result.filtered_length == len(text)
    assert result.interval_sequences[2] == "12345"


def test_extract_skip_sequences_preserve_case():
    text = "AbCDefGHi"
    result = extract_skip_sequences(text, [2], uppercase=False)

    assert result.filtered_length == len(text)
    assert result.interval_sequences[2] == "bDfH"
