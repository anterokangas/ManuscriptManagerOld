import pytest
from manuscript.tools.quotes import add_quotes
from manuscript.tools.quotes import remove_quotes


def test_add_quotes():
    assert add_quotes("abc") == "abc"
    assert add_quotes("abc def") == '"abc def"'
    assert add_quotes("abc \"def\"") == "'abc \"def\"'"
    assert add_quotes("abc\"def\"") == "abc\"def\""
    assert add_quotes("abc\" def\"") == "'abc\" def\"'"
    assert add_quotes("abc'cde\"fgg") == "abc'cde\"fgg"
    assert add_quotes("abc 'cde\"fgg") == '"abc \'cde\"fgg"'

def test_remove_quotes():
    assert remove_quotes("") == ""
    assert remove_quotes("a") == "a"
    assert remove_quotes("ab") == "ab"
    assert remove_quotes("abc") == "abc"
    assert remove_quotes("'abc'") == "abc"
    assert remove_quotes('"abc"') == "abc"
    assert remove_quotes("abc def") == "abc def"
    assert remove_quotes("'") == "'"
    assert remove_quotes("''") == ""
    assert remove_quotes("'''") == "'"
    assert remove_quotes("'\"'") == "\""
    assert remove_quotes('"') == '"'
    assert remove_quotes('""') == ''
    assert remove_quotes('"""') == '"'
    assert remove_quotes('"\'"') == "\'"
    assert remove_quotes("'abc \"def\"'") == "abc \"def\""
    assert remove_quotes("abc\"def\"") == "abc\"def\""
    assert remove_quotes("'abc\" def\"'") == "abc\" def\""
    assert remove_quotes("abc'cde\"fgg") == "abc'cde\"fgg"