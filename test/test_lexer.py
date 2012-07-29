import re
from plist.lexer import LexerGrammar, Pattern, Lexer
import sys
if sys.version_info >= (2,7):
    import unittest
else:
    import unittest2 as unittest

testGrammarDefinition = (
    ("COMMENT", r"//.*$"),
    ("COMMENT_MULTILINE", r"/\*.*\*/"),
    ("WHITESPACE", r"\s+"),
    ("DELIMITER", r";"),
    ("ELEMENT_SEPERATOR", r","),
    ("ASSIGNMENT", r"="),
    ("BRACKET_OPEN", r"\("),
    ("BRACKET_CLOSE", r"\)"),
    ("BRACE_OPEN", r"\{"),
    ("BRACE_CLOSE", r"\}"),
    ("STRING", r'\"(([^\\"]|(\\"|\\\\)))*\"'),
    ("IDENTIFIER", r"([^;\s=\(\)\{\}\,\"]+)")
)

EXPECTED_TOKENS = (
    "COMMENT_MULTILINE", 
    "BRACE_OPEN",
    "IDENTIFIER", "ASSIGNMENT", "STRING", "DELIMITER",
    "IDENTIFIER", "ASSIGNMENT", "BRACKET_OPEN", "IDENTIFIER", "ELEMENT_SEPERATOR", "IDENTIFIER", "BRACKET_CLOSE",
    "BRACE_CLOSE")

class LexerTest(unittest.TestCase):
    def test_simpleLexerTest(self):
        testGrammar = LexerGrammar()
        for (name, expression) in testGrammarDefinition:
            testGrammar.add_pattern(name, expression)
        testLexer = Lexer(testGrammar)

        testInput = """/* !UTF-8 */
        {
            meaningoflive = "1234";
            somearrayman = (1,2)
        }
        """

        matchedTokens = list(testLexer.scan(testInput))
        comparedTokenNames = [token.name for token in matchedTokens if token.name != "WHITESPACE"]

        for index, (expected, actual) in enumerate(zip(EXPECTED_TOKENS, comparedTokenNames)):
            self.assertEquals(expected, actual, "expected token %s but got %s instead at index %d" % (expected, actual, index))
