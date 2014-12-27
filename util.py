# Utility stuff

def tounicode(x):
    """Convert something to unicode."""
    if isinstance(x, unicode):
        return x
    if isinstance(x, str):
        return x.decode('utf8')
    return unicode(x)

def toutf8(x):
    """Convert something to UTF-8."""
    if isinstance(x, unicode):
        return x.encode('utf8')
    if isinstance(x, str):
        return x
    return str(x)
