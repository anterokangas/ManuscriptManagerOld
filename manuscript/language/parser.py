"""
Manuscript Manager
Syntax parser
"""
from sly import Parser
from manuscript.language.lexer import ManuscriptLexer

from manuscript.language.process_command import process_command

import manuscript.tools.constants as mc
import manuscript.exceptions.exceptions as mex


class ManuscriptParser(Parser):
    """ Syntax parser
    manuscript ::= manuscript part | part
    part ::= command | values
    command ::= NAME values _params ')' | NAME _params ')' | NAME values ')' | NAME ')' |
    _params ::= _params param | param
    param ::= NAME values ')'
    values ::= values STRING | STRING
    NAME ::= "("+string_without \s, (, ), ", ', @, #, %, *
    STRING ::= "..." | '...' | string not starting by ( and not having \s, (, ), ", ', @
    comment ::= (*...*) | (#...#) | (%...%)
    """
    # debugfile = "parser.out"
    tokens = ManuscriptLexer.tokens

    def error(self, p):
        if not p:
            raise mex.MMSyntaxError("*** SyntaxError: EOF encountered too early")
        raise mex.MMSyntaxError(f"*** SyntaxError {p}")

    def __init__(self, work):
        """ initialization """
        self.work = work

    @_('manuscript part')
    def manuscript(self, p):
        return p.manuscript if p.part is None else p.manuscript + [p.part]

    @_('part')
    def manuscript(self, p):
        return [p.part]

    @_('command')
    def part(self, p):
        return p.command

    @_('values')
    def part(self, p):
        return mc.NARRATOR, self.work.defined_actions[mc.NARRATOR], {mc.VALUES: p.values}

    @_('NAME values _params RPAREN')
    def command(self, p):
        name = p.NAME[1:].strip()
        params = p.params
        values = p.values  # _params.pop(mc.VALUES, "")
        line_number = p.lineno
        return process_command(name, params, values, line_number, self.work)

    @_('NAME _params RPAREN')
    def command(self, p):
        name = p.NAME[1:].strip()
        params = p.params
        values = ""  # p.values  # _params.pop(mc.VALUES, "")
        line_number = p.lineno
        return process_command(name, params, values, line_number, self.work)

    @_('NAME values RPAREN')
    def command(self, p):
        name = p.NAME[1:].strip()
        params = {}
        values = p.values  # _params.pop(mc.VALUES, "")
        line_number = p.lineno
        return process_command(name, params, values, line_number, self.work)

    @_('NAME RPAREN')
    def command(self, p):
        name = p.NAME[1:].strip()
        params = {}
        values = ""  # _params.pop(mc.VALUES, "")
        line_number = p.lineno
        return process_command(name, params, values, line_number, self.work)

    @_('_params param')
    def params(self, p):
        return {**p.params, **p.param} if list(p.param.keys())[0] not in p.params.keys() else p.params

    @_('param')
    def params(self, p):
        return p.param

    # @_('empty')
    # def _params(self, p):
    #     return {}
    #
    # @_('')
    # def empty(self, p):
    #     pass

    # @_('values')
    # def _params(self, p):
    #     return {mc.VALUES: p.values}

    @_('NAME values RPAREN')
    def param(self, p):
        name = p.NAME[1:].strip()
        values = p.values
        return {name: values}

    @_('values STRING')
    def values(self, p):
        return p.values + " " + p.STRING

    @_('STRING')
    def values(self, p):
        return p.STRING



def p_error(p):
    if p:
        raise mex.MMSyntaxError("*** Syntax error at token {p.type}, line {p.lineno}")
    else:
        raise mex.MM.SyntaxError("*** Syntax Error at EOF, line {p.lineno}")