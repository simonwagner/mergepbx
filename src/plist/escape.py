import re

CONTROL_CHARS = {
    u"\n" : u"\\n",
    u"\t" : u"\\t",
    u"\"" : u"\\\"",
    u"\\" : u"\\\\",
}

ESCAPED_CHARS = dict((value, key) for key, value in CONTROL_CHARS.iteritems())

CONTROL_CHAR_RE = re.compile(
    unicode.join(u"|", (u"(%s)" % re.escape(char) for char in CONTROL_CHARS.iterkeys()))
)

ESCAPED_CHARS_RE = re.compile(
    unicode.join(u"|", (u"(%s)" % re.escape(char) for char in ESCAPED_CHARS.iterkeys()))
)

def escape_string(s):
    escaped_s = CONTROL_CHAR_RE.sub(
        lambda match: CONTROL_CHARS[match.group()],
        s
    )
    return escaped_s

def unescape_string(s):
    unescaped_s = ESCAPED_CHARS_RE.sub(
        lambda match: ESCAPED_CHARS[match.group()],
        s
    )
    return unescaped_s
