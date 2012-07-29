from .tree import TreeBuilder
from .tokenstream import TokenStream
import logging

logger = logging.getLogger("plist.parser.parser")

class ParserGrammar(object):
    def __init__(self, rules, ignore_tokens = []):
        self.rules = dict((rule.name, rule) for rule in rules)
        self.ignore_tokens = ignore_tokens

    def get_rule(self, rule_name):
        return self.rules[rule_name]

class Parser(object):
    def __init__(self, grammar, lexer):
        self.grammar = grammar
        self.lexer = lexer

    def parse(self, starting_symbol, input, tree_builder_class = TreeBuilder):
        token_stream = TokenStream(self.lexer, input, self.grammar.ignore_tokens)

        starting_rule = self.grammar.get_rule(starting_symbol)
        tree_builder = tree_builder_class(starting_rule)

        logger.info("matching starting_symbol %s", starting_symbol)
        success = starting_rule.match(self, tree_builder, token_stream)

        if success:
            logger.info("input matched starting_symbol %s", starting_symbol)
            tree = tree_builder.build()
            return tree
        else:
            logger.info("input does not match %s", starting_symbol)
            return None

    def get_rule(self, rule_name):
        return self.grammar.get_rule(rule_name)
