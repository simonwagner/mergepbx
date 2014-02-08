import re

CONTROL_CHARS = {
    u"\n" : u"\\n",
    u"\t" : u"\\t",
    u"\"" : u"\\\"",
    u"\\" : u"\\\\",
}

CONTROL_CHAR_RE = re.compile(
    unicode.join(u"|", (u"(%s)" % re.escape(char) for char in CONTROL_CHARS.iterkeys()))
)

def escape_string(s):
    escaped_s = CONTROL_CHAR_RE.sub(
        lambda match: CONTROL_CHARS[match.group()],
        s
    )
    return escaped_s
