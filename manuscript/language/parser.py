"""
Manuscript Manager
Syntax parser
"""
from sly import Parser
from manuscript.language.lexer import ManuscriptLexer
import manuscript.tools.constants as mc
from manuscript.language.process_command import process_command


class ManuscriptParser(Parser):
    """ Syntax parser
    manuscript ::= manuscript part | part
    part ::= command | values
    command ::= name params ')'
    params ::= params param | param | empty
    param ::= name values ')' | values
    values ::= values STRING | STRING
    STRING ::= "..." | '...' | non-terminal string
    comment ::= (*...*) | (#...#) | (%...%)
    """
    debugfile = "parser.out"
    tokens = ManuscriptLexer.tokens

    def __init__(self, producer):
        """ initialization """
        self.producer = producer

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
        return mc.NARRATOR, self.producer.defined_actions[mc.NARRATOR], {mc.VALUES: p.values}

    @_('NAME params RPAREN')
    def command(self, p):
        name = p.NAME[1:].strip()
        params = p.params
        values = params.pop(mc.VALUES, "")
        line_number = p.lineno
        return process_command(name, params, values, line_number, self.producer)

    @_('params param')
    def params(self, p):
        return {**p.params, **p.param} if list(p.param.keys())[0] not in p.params.keys() else p.params

    @_('param')
    def params(self, p):
        return p.param

    @_('empty')
    def params(self, p):
        return {}

    @_('')
    def empty(self, p):
        pass

    @_('values')
    def params(self, p):
        return {mc.VALUES: p.values}

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
