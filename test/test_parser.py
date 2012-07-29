from plist.parser import ParserGrammar, Parser, Rule, Terminal, NonTerminal, TokenStream
import re
from plist.lexer import LexerGrammar, Pattern, Lexer
import sys
if sys.version_info >= (2,7):
    import unittest
else:
    import unittest2 as unittest
import difflib
import plist.nextstep

testLexerGrammar = plist.nextstep.LEXER_GRAMMAR
testParserGrammar = plist.nextstep.PARSER_GRAMMAR

class ParserTest(unittest.TestCase):
    pass
