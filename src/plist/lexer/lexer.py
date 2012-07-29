import re
from collections import namedtuple, OrderedDict
import logging
from itertools import chain

Token = namedtuple("Token", ("name", "match"))
Pattern = namedtuple("Pattern", ("name", "pattern"))

class Lexer(object):
    def __init__(self, lexer_grammar):
        self.lexer_grammar = lexer_grammar
        self.logger = logging.getLogger("plist.lexer")

    def scan(self, input):
        current_part = input
        while len(current_part) > 0:
            for name, pattern in self.lexer_grammar:
                match = pattern.match(current_part)
                if match:
                    matched_string = match.group()
                    self.logger.info("pattern %s matches '%s'", name, matched_string)
                    break

            if not match:
                self.logger.error("no pattern matched")
                raise Exception("unrecognizable token at '%s'" % (current_part))
            else:
                yield Token(name, match)
                match_length = len(matched_string)
                current_part = current_part[match_length:]

class LexerGrammar(object):
    def __init__(self, patterns = ()):
        self.rules = OrderedDict(self.make_pattern(name, expr) for (name, expr) in patterns)

    def make_pattern(self, name, pattern_expression):
        return Pattern(name, re.compile(pattern_expression, re.MULTILINE | re.DOTALL))

    def add_pattern(self, name_or_pattern, pattern_expression=None):
        if pattern_expression == None:
            pattern = name_or_pattern
        else:
            pattern = self.make_pattern(name_or_pattern, pattern_expression)

        self.rules[pattern.name] = pattern.pattern
        return self

    def __iter__(self):
        return self.rules.iteritems()