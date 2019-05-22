from manuscript.language.lexer import ManuscriptLexer
from manuscript.language.parser import ManuscriptParser
from manuscript.actions.definition import Definition
from manuscript.actions.role import Role
import manuscript.tools.constants as mc


lexer = ManuscriptLexer()
parser = ManuscriptParser()
Definition.defined_actions[mc.NARRATOR] = Role(name=mc.NARRATOR, lang='en')


def test_commands():
    text = """Role A"""
    pp = parser.parse(lexer.tokenize(text))
    assert pp[0][0] == mc.NARRATOR and \
        isinstance(pp[0][1], Role) and \
        pp[0][2] == {mc.VALUES: 'Role A'}

    text = """(Role A)"""
    pp = parser.parse(lexer.tokenize(text))
    assert pp == [('Role', None, {mc.VALUES: 'A'})]

    text = """(Role A (param1 1))"""
    pp = parser.parse(lexer.tokenize(text))
    assert pp == [('Role', None, {mc.VALUES: 'A', 'param1': '1'})]

    text = """(Role A B (param1 1 2 "xy z" (# string continues! #) 'a b c'))"""
    pp = parser.parse(lexer.tokenize(text))
    assert pp == [('Role', None, {mc.VALUES: 'A B', 'param1': '1 2 "xy z" \'a b c\''})]

    text = """(A (param1 1))"""
    pp = parser.parse(lexer.tokenize(text))
    assert pp == [('A', None, {mc.VALUES: '', 'param1': '1'})]

    text = """(A)"""
    pp = parser.parse(lexer.tokenize(text))
    assert pp == [('A', None, {mc.VALUES: ''})]

    text = """(Role A (param1 1))
    (A text (lang en))"""
    pp = parser.parse(lexer.tokenize(text))
    assert pp == [('Role', None, {mc.VALUES: 'A', 'param1': '1'}),
                  ('A', None, {mc.VALUES: 'text', 'lang': 'en'})]


if __name__ == "__main__":
    test_commands()

