from gvet.gv import search_utils


def test_add_wildcard():
    words = "bear market socks".split(" ")
    modified = search_utils.add_wildcard(words)
    assert " ".join(modified) == "bear* market* socks*"


def test_add_conjunction():
    words = "bear market socks".split(" ")
    modified = search_utils.add_conjunction(words)
    assert " ".join(modified) == "bear AND market AND socks"


def test_remove_stop_words():
    words = "billy the kid".split(" ")
    modified = search_utils.remove_stop_words(words)
    assert " ".join(modified) == "billy kid"
