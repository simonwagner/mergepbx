from plist.parser.tokenstream import TokenStream, BacktrackingTokenStream, TokenIter
from plist.lexer import Token

import re
from plist.lexer import LexerGrammar, Pattern, Lexer
import sys
if sys.version_info >= (2,7):
    import unittest
else:
    import unittest2 as unittest
from itertools import islice

class LexerMock(object):
    def __init__(self, tokens):
        self.tokens = tokens
    def scan(self, input):
        return iter(self.tokens)

class TokenStreamTest(unittest.TestCase):
    def test_peeking_with_backtracking(self):
        tokens = [Token("A", "a"), Token("B", "b"), Token("C", "c")]
        stream = TokenStream(LexerMock(tokens), "")
        bt_stream = BacktrackingTokenStream(stream)

        bt_stream.backtrack()
        self.assertEqualTokens(bt_stream.peek()[0], Token("A","a"))
        bt_stream.success()
        self.assertEqualTokens(stream.peek()[0], Token("A","a"))

    def test_peeking(self):
        tokens = [Token("A", "a"), Token("B", "b"), Token("C", "c")]
        stream = TokenStream(LexerMock(tokens), "")
        self.assertEqualTokens(stream.peek()[0], Token("A","a"))
        self.assertEqualTokens(stream.peek()[0], Token("A","a"))

    def test_token_iter(self):
        tokens = [Token("A", "a"), Token("B", "b"), Token("C", "c")]
        token_iter = TokenIter(iter(tokens))

        read_tokens = list(islice(token_iter, 0, 1))
        token_iter.push_tokens(read_tokens)

        for actual_token, expected_token in zip(token_iter, tokens):
            self.assertEqualTokens(actual_token, expected_token)

    def assertEqualTokens(self, actual, expected):
        self.assertEquals(actual.name, expected.name)
        self.assertEquals(actual.match, expected.match)

if __name__ == '__main__':
    unittest.main()
