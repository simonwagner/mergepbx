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
        self.expected = None
        self.count_expected_matched = 0
        self.count_matches = 0

    def expect(self, expected):
        self.expected = expected

    def scan(self, input):
        current_part = input
        while len(current_part) > 0:
            token_match = self.match(current_part, self.expected)
            self.expected = None #clear expected token after trying to match it

            if not token_match:
                self.logger.error("no pattern matched")
                raise Exception("unrecognizable token at '%s'" % (current_part))
            else:
                name, match = token_match
                matched_string = match.group()

                self.logger.info("pattern %s matches '%s'", name, matched_string)
                yield Token(name, match)

                match_length = len(matched_string)
                current_part = current_part[match_length:]

    def hit_rate_for_expected(self):
        return self.count_expected_matched/float(self.count_matches)

    def match(self, input, expected = None):
        self.count_matches += 1
        if not expected is None:
            match_with_expected = self.match_expected(input, expected)
            if not match_with_expected is None:
                return match_with_expected

        return self.match_any(input)

    def match_expected(self, input, expected):
        name, pattern = self.lexer_grammar.get_pattern(expected)
        match = pattern.match(input)

        if match:
            self.count_expected_matched += 1
            return (name, match)
        else:
            return None

    def match_any(self, input):
        for name, pattern in self.lexer_grammar:
            match = pattern.match(input)
            if match:
                return (name, match)

        return None

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

    def get_pattern(self, name):
        return (name, self.rules.get(name, None))

    def __iter__(self):
        return self.rules.iteritems()