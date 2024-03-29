"""
Manuscript Manager
Lexical analyser
"""
from sly import Lexer

from manuscript.language.find_column import find_column
#from manuscript.tools.highlight import highlight
import manuscript.exceptions.exceptions as mex

class ManuscriptLexer(Lexer):
    """ Lexical analyser """

    tokens = (NAME, STRING, RPAREN)
    ignore = ' \t'
    ignore_r = r'\r'  # if UTF-8 encoding
    ignore_hashcomment = r'\(\#(?s)(.*?)\#\)'      # (#...#)
    ignore_percentcomment = r'\(%(?s)(.*?)%\)'     # (%...%)
    ignore_asteriskcomment = r'\(\*(?s)(.*?)\*\)'  # (*...*)

    NAME = r'\(\s*[^\s\#%*@\*"\'\(\)]+'  # starts with (, no ", ', {, ), #, %, *
    RPAREN = r'\)'
    STRING = (
        r'"[^"]*"'           # double quote string
        r"|'[^']*'"          # single quote string
        r'|[^\s@"\'\(\)]+'   # no \s, @, ", ', (, )
    )

    # @_(r'\(\s*[^\s\#%*@\*"\'\(\)]+')
    # def NAME(self, t):
    #     t.value = t.value.upper()
    #     return t

    @_(r'@(?s)(.*)')
    def eof(self, t):
        """ End-of-file: @ causes eof (for debugging purposes)
        :param t: token
        :return: None
        """
        pass

    @_(r'\n+')
    def newline(self, t):
        """ handle newlines
        :param t: token
        :return: None
        """
        self.lineno += t.value.count('\n')

    def error(self, t):
        """ Notify errors
        :param t: token
        :return: error, increase index
        """
        ill_char = ascii(t.value[0])
        raise mex.MMSyntaxError(f"*** Lexical error: illegal character {ill_char} in line {self.lineno}")

        print(highlight(
            f"*** Lexical error: illegal character '{ill_char}' in line {self.lineno}",
            color='red'))
        self.index += 1


if __name__ == "__main__":
    lexer = ManuscriptLexer()
    text = """(* this is a comment *)
              (Role A (lang en))
           """
    tokens = lexer.tokenize(text)
    print(f"tokens={list(tokens)}")