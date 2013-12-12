from plist.parser import ParserGrammar, Parser, Rule, Terminal, NonTerminal, TokenStream
import re
from plist.lexer import LexerGrammar, Pattern, Lexer
from plist.parser import ParserGrammar, Parser, Rule, Terminal, NonTerminal
from plist.parser.tree import AbstractObjectTreeBuilder
from collections import OrderedDict

IDENTIFIER_RE = r"^([^;\s=\(\)\{\}\,\"\<\>]+)$"
LEXER_GRAMMAR = LexerGrammar((
    ("COMMENT_SINGLELINE", r"//.*?$"),
    ("COMMENT", r"/\*.*?\*/"),
    ("WHITESPACE", r"\s+"),
    ("DICTIONARY_SEPERATOR", r";"),
    ("ARRAY_SEPERATOR", r","),
    ("ASSIGNMENT", r"="),
    ("BRACKET_OPEN", r"\("),
    ("BRACKET_CLOSE", r"\)"),
    ("BRACE_OPEN", r"\{"),
    ("BRACE_CLOSE", r"\}"),
    ("STRING", r'\"((([^\\"]|(\\.)))*)\"'),
    ("IDENTIFIER", r"([^;\s=\(\)\{\}\,\"\<\>]+)")
))

PARSER_GRAMMAR = ParserGrammar((
    Rule("plist", NonTerminal("dictionary") | NonTerminal("array")),
    Rule("value", NonTerminal("dictionary") | NonTerminal("array") | Terminal("IDENTIFIER") | Terminal("STRING")),
    Rule("array", 
        Terminal("BRACKET_OPEN") + \
            (
                NonTerminal("value") + (Terminal("ARRAY_SEPERATOR") + NonTerminal("value")).repeat().optional() + Terminal("ARRAY_SEPERATOR").optional()
            ).optional() + \
        Terminal("BRACKET_CLOSE")
    ),
    Rule("dictionary_entry", (Terminal("IDENTIFIER") | Terminal("STRING")) + Terminal("ASSIGNMENT") + NonTerminal("value") + Terminal("DICTIONARY_SEPERATOR")),
    Rule("dictionary", 
        Terminal("BRACE_OPEN") + \
            (
                NonTerminal("dictionary_entry").repeat()
            ).optional() + \
        Terminal("BRACE_CLOSE")
    ),
),
ignore_tokens=["COMMENT", "COMMENT_SINGLELINE", "WHITESPACE"]
)

class NSPlistTreeBuilder(AbstractObjectTreeBuilder):
    def build_plist(self, node):
        assert(len(node.children) == 1)

        first_child = next(iter(node.children))

        return first_child.object

    def build_dictionary(self, node):
        entry_children = (child for child in node.children if child.value.name == "dictionary_entry")
        return OrderedDict(child.object for child in entry_children)

    def build_dictionary_entry(self, node):
        first_child = next(iter(node.children))

        key = first_child.object

        for child in node.children:
            if child.value.name == "value":
                value = child.object

        return (key, value)

    def build_value(self, node):
        first_child = next(iter(node.children))
        return first_child.object

    def build_array(self, node):
        entry_children = (child.object for child in node.children if child.value.name == "value")

        return list(entry_children)

    def build_IDENTIFIER(self, node):
        return node.value.match.group(1)

    def build_STRING(self, node):
        string = node.value.match.group(1)
        string_value = string.decode("string_escape")
        return string_value

class NSPlistReader(object):
    def __init__(self, f):
        self.f = f

    def read(self):
        plist_lexer = Lexer(LEXER_GRAMMAR)
        plist_parser = Parser(PARSER_GRAMMAR, plist_lexer)

        tree = plist_parser.parse("plist", self.f.read(), tree_builder_class = NSPlistTreeBuilder)

        if not tree:
            raise Exception("can't parse plist")

        return tree.root.object

    def close(self):
        self.f.close()

class NSPlistWriter(object):
    def __init__(self, f, codec="UTF-8"):
        self.f = f
        self.codec = codec

    def write(self, data):
        self.f.write("// !$*%s*$!\n" % self.codec)
        self.walk_plist(self.f, data)

    def walk_plist(self, f, data):
        if hasattr(data, "iteritems"):
            self.walk_dictionary(f, data.iteritems())
        elif hasattr(data, "__iter__"):
            self.walk_array(f, data)
        else:
            raise Exception("unknown data type, must be either a dictionary or an array")

    def walk_dictionary(self, f, items):
        f.write("{")
        for key, value in items:
            key_bytes = key.encode(self.codec)
            f.write("\"%s\" = " % key_bytes.encode("string_escape"))
            self.walk_value(f, value)
            f.write("; ")
        f.write("}\n")

    def walk_array(self, f, items):
        f.write("(")
        for item in items:
            self.walk_value(f, item)
            f.write(", ")
        f.write(")\n")

    def walk_value(self, f, data):
        if hasattr(data, "iteritems"):
            self.walk_dictionary(f, data.iteritems())
        elif hasattr(data, "__iter__"):
            self.walk_array(f, data)
        else:
            f.write("\"%s\"" % str(data).encode("string_escape"))