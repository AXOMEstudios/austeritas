from src.helpers import validate_player_name


def test_malicious_input():
    MALICIOUS = [
        "; stop",
        "; give @a diamond_block 64",
        "rm -r /",
        "/kill Player2321"
    ]
    for inp in MALICIOUS:
        assert not validate_player_name(inp)

def test_invalid_input():
    INVALID = [
        "§$)(/(%&))",
        "13754FHuiwb§(,)",
        "...Aplayerubr",
        "RAAANDOMSTRING$)()",
        "!__EUDFB"
    ]
    for inp in INVALID:
        assert not validate_player_name(inp)

def test_no_input():
    assert not validate_player_name("")

def test_short_input():
    INVALID = [
        "§$",
        "13",
        "_T",
        "R",
        "La",
        "m"
    ]
    for inp in INVALID:
        assert not validate_player_name(inp)

def test_correct_input():
    VALID = [
        "Player mrcool",
        "EpicGamer281",
        "Ohye",
        "Valid_guy",
        "yee_2_2r"
    ]
    for inp in VALID:
        assert validate_player_name(inp)
        