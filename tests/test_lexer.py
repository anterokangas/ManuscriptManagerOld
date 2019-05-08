from manuscript.language.lexer import ManuscriptLexer

lexer = ManuscriptLexer()

def test_tokens():
    text = """(Role """
    tokens = list(lexer.tokenize(text))
    assert tokens[0].type == "NAME" and \
           tokens[0].value == "(Role" and \
           len(tokens) == 1

    text = """A"""
    tokens = list(lexer.tokenize(text))
    assert tokens[0].type == "STRING" and \
           tokens[0].value == "A" and \
           len(tokens) == 1

    text = """'A'"""
    tokens = list(lexer.tokenize(text))
    assert tokens[0].type == "STRING" and \
           tokens[0].value == "'A'" and \
           len(tokens) == 1

    text = '''"A"'''
    tokens = list(lexer.tokenize(text))
    assert tokens[0].type == "STRING" and \
           tokens[0].value == '"A"' and \
           len(tokens) == 1

    text = """)"""
    tokens = list(lexer.tokenize(text))
    assert tokens[0].type == "RPAREN" and \
           tokens[0].value == ")" and \
           len(tokens) == 1


def test_ignores():
    lexer = ManuscriptLexer()

    text = ""
    tokens = list(lexer.tokenize(text))
    assert len(tokens) == 0

    text = " "
    tokens = list(lexer.tokenize(text))
    assert len(tokens) == 0

    text = "\t"
    tokens = list(lexer.tokenize(text))
    assert len(tokens) == 0

    text = " \t\t\t\t    \t "
    tokens = list(lexer.tokenize(text))
    assert len(tokens) == 0


def test_comments():
    lexer = ManuscriptLexer()

    text = "(# Hash comment #)"
    tokens = list(lexer.tokenize(text))
    assert len(tokens) == 0

    text = "(% Percent comment %)"
    tokens = list(lexer.tokenize(text))
    assert len(tokens) == 0

    text = "(* Asterisk comment *)"
    tokens = list(lexer.tokenize(text))
    assert len(tokens) == 0

    text = "(# (# (# Hash comment #)"
    tokens = list(lexer.tokenize(text))
    assert len(tokens) == 0

    text = "(# %) Hash comment #)"
    tokens = list(lexer.tokenize(text))
    assert len(tokens) == 0

    text = "(# *) Hash comment #)"
    tokens = list(lexer.tokenize(text))
    assert len(tokens) == 0


if __name__ == "__main__":
    test_tokens()
    test_ignores()
    test_comments()
