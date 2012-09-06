from .tokenstream import BacktrackingTokenStream
import logging

logger = logging.getLogger("plist.parser.rules")

#rules
class RuleElement(object):
    def __init__(self):
        pass

    def repeat(self):
        return RepeatedRule(self)

    def optional(self):
        return OptionalRule(self)

    def __add__(rule1, rule2):
        if isinstance(rule1, ConcatinatedRules) and isinstance(rule2, ConcatinatedRules):
            return ConcatinatedRules(rule1.rules + rule2.rules)
        else:
            return ConcatinatedRules((rule1, rule2))

    def __or__(rule1, rule2):
        if isinstance(rule1, AlternativeRules) and isinstance(rule2, AlternativeRules):
            return AlternativeRules(rule1.rules + rule2.rules)
        else:
            return AlternativeRules((rule1, rule2))

class ConcatinatedRules(RuleElement):
    def __init__(self, rules):
        self.rules = rules

    def match(self, parser, tree_builder, token_stream):
        matches = True
        backtracking_token_stream = BacktrackingTokenStream.create(token_stream)
        backtracking_token_stream.backtrack()

        for rule in self.rules:
            if not rule.match(parser, tree_builder, token_stream):
                matches = False
                break

        if not matches:
            #restore previous state
            backtracking_token_stream.fail()
        else:
            backtracking_token_stream.success()

        del backtracking_token_stream
        return matches

    def __repr__(self):
        rules_repr = [repr(rule) for rule in self.rules]
        return "<ConcatenatedRules %s" % " + ".join(rules_repr)

class AlternativeRules(RuleElement):
    def __init__(self, rules):
        self.rules = rules

    def match(self, parser, tree_builder, token_stream):
        backtracking_token_stream = BacktrackingTokenStream.create(token_stream)

        for rule in self.rules:
            backtracking_token_stream.backtrack()

            matches = rule.match(parser, tree_builder, token_stream)
            if matches:
                backtracking_token_stream.success()
                logger.debug("%s matches of the alternatives in %r", rule, self.rules)
                del backtracking_token_stream
                return True
            else:
                backtracking_token_stream.fail()

        logger.debug("No alternative matches of %r", self.rules)
        backtracking_token_stream.fail()
        del backtracking_token_stream
        return False

    def __repr__(self):
        rules_repr = [repr(rule) for rule in self.rules]
        return "<AlternativeRules %s>" % " | ".join(rules_repr)

class RepeatedRule(RuleElement):
    def __init__(self, rule):
        self.rule = rule

    def match(self, parser, tree_builder, token_stream):
        backtracking_token_stream = BacktrackingTokenStream.create(token_stream)

        count_matches = 0
        logger.debug("trying to match multiple times")
        while True:
            backtracking_token_stream.backtrack()
            matches = self.rule.match(parser, tree_builder, backtracking_token_stream)
            if matches:
                backtracking_token_stream.success()
                count_matches += 1
            else:
                logger.debug("repitition failed, stopped repeating")
                backtracking_token_stream.fail()
                break
            logger.debug("repitition, trying again")

        del backtracking_token_stream
        logger.debug("repitition matched %d times", count_matches)

        return count_matches > 0

    def __repr__(self):
        return "<RepeatedRule %r>" % self.rule

class OptionalRule(RuleElement):
    def __init__(self, rule):
        self.rule = rule

    def match(self, parser, tree_builder, token_stream):
        backtracking_token_stream = BacktrackingTokenStream.create(token_stream)
        backtracking_token_stream.backtrack()
        matches = self.rule.match(parser, tree_builder, backtracking_token_stream)
        logger.debug("testing optional rule")
        if matches:
            logger.debug("optional rule matches")
            backtracking_token_stream.success()
        else:
            logger.debug("optional rule does not match")
            backtracking_token_stream.fail()

        del backtracking_token_stream
        return True

    def __repr__(self):
        return "<OptionalRule %r>" % self.rule

class Terminal(RuleElement):
    def __init__(self, token_name):
        self.expected_token_name = token_name

    def match(self, parser, tree_builder, token_stream):
        token_stream.expect(self.expected_token_name)

        tokens = token_stream.peek(1)
        token = tokens[0] if len(tokens) > 0 else None
        logger.debug("matching terminal %s" % self.expected_token_name)
        if token != None and token.name == self.expected_token_name:
            token_stream.pop()
            tree_builder.down(token)
            tree_builder.up()
            logger.debug("matched terminal %s" % self.expected_token_name)
            return True
        else:
            if token != None:
                logger.debug("matching terminal failed: got %s", token.name)
            else:
                logger.debug("no more tokens available to match")
            return False

    def __repr__(self):
        return "<Terminal %s>" % (self.expected_token_name)

class NonTerminal(RuleElement):
    def __init__(self, rule_name):
        self.expected_rule_name = rule_name

    def match(self, parser, tree_builder, token_stream):        
        rule = parser.get_rule(self.expected_rule_name)
        logger.debug("matching non-terminal %r: %r", rule, rule.rule_definition)
        tree_builder.down(rule)
        if rule.match(parser, tree_builder, token_stream):
            tree_builder.up()
            logger.debug("matched non-terminal %r", rule)
            return True
        else:
            tree_builder.delete()
            return False

    def __repr__(self):
        return "<NonTerminal %s>" % (self.expected_rule_name)

class Rule(RuleElement):
    def __init__(self, rule_name, rule_definition):
        self.name = rule_name
        self.rule_definition = rule_definition

    def match(self, parser, tree_builder, token_stream):
        match_result = self.rule_definition.match(parser, tree_builder, token_stream)

        return match_result

    def __repr__(self):
        return "<Rule %s>" % self.name
