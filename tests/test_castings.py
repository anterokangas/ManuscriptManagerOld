from manuscript.tools.castings import bool_
from manuscript.tools.castings import list_
from manuscript.tools.castings import as_is


def test_bool_():
    assert bool_(False) is False
    assert bool_(True) is True

    assert bool_("False") is False
    assert bool_("FALSE") is False
    assert bool_("FaLsE") is False
    assert bool_("false") is False
    assert bool_("F") is False
    assert bool_("f") is False

    assert bool_("") is False
    assert bool_(" ") is False

    assert bool_("True") is True
    assert bool_("TRUE") is True
    assert bool_("TrUe") is True
    assert bool_("true") is True
    assert bool_("T") is True
    assert bool_("t") is True
    assert bool_("X") is True
    assert bool_("Xyzzy") is True

    assert bool_(0) is False
    assert bool_(1) is False
    assert bool_(100) is False
    assert bool_(-10) is False
    assert bool_([]) is False
    assert bool_([True]) is False
    assert bool_(()) is False
    assert bool_((True,)) is False
    assert bool_({'a': True}) is False
    assert bool_({}) is False
    assert bool_(set()) is False
    assert bool_({True}) is False
    assert bool_(None) is False


def test_list_():
    assert list_("") == ['']
    assert list_("a b c dfg") == ['a', 'b', 'c', 'dfg', '']
    assert list_("a 'b c' dfg") == ['a', "'b c'", 'dfg', '']
    assert list_('a "b c" dfg') == ['a', '"b c"', 'dfg', '']
    assert list_(' a  "b c" dfg' + " 'h i j' ") == ['a', '"b c"', 'dfg', "'h i j'", '']


def test_as_is():
    assert as_is(None) is None
    assert as_is("Xyzzy") == "Xyzzy"
