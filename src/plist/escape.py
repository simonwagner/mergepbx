def escape_string(s):
    escaped_s = s.encode("string_escape")
    #replace " with \", because string_escape does not do this
    escaped_s = escaped_s.replace("\"", "\\\"")
    #replace \' with ', because that is acceptable
    escaped_s = escaped_s.replace("\\'", "'")
    return escaped_s
