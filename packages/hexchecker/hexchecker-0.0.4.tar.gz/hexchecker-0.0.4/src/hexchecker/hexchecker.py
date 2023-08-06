"""
hexchecker
https://github.com/xhelphin/hexchecker

Simple Python package to check if string is valid hexadecimal.
"""

def hexchecker(string):
    """
    Returns True if string is valid hexidecimal with any character case, else returns False.
    """
    for character in string:
        if '0' <= character <= '9':
            continue
        if 'a' <= character <= 'f':
            continue
        if 'A' <= character <= 'F':
            continue
        return False
    return True

def hexcheckerLower(string):
    """
    Returns True if string is valid hexidecimal with lowercase characters, else returns False.
    """
    for character in string:
        if '0' <= character <= '9':
            continue
        if 'a' <= character <= 'f':
            continue
        return False
    return True

def hexcheckerUpper(string):
    """
    Returns True if string is valid hexidecimal with uppercase characters, else returns False.
    """
    for character in string:
        if '0' <= character <= '9':
            continue
        if 'A' <= character <= 'F':
            continue
        return False
    return True