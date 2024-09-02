from typing import *
from copy import copy
from collections import deque
import re


def expandtoken(s):
    p = re.compile("([0-9]+)\[([^0-9]+)\]")
    groups = p.match(s)
    if groups:
        _m = groups.group(1)
        _s = groups.group(2)
        return _s * int(_m)
    return "<error>"


def reassemble(s, inject, idx_start, idx_end):
    # We cut out substring from idx_start to idx_end and replace it with the new inject substring
    r = s[:idx_start] + inject + s[idx_end:]
    return r

def extracttoken(s):
    # this func will extract first encountered fully formed [0-9]+\[[^0-9]+\] token from the given string and return starting position of that token in the string
    # so that it can be replaced in-place
    token_end = s.find("]")
    token_start = s[:token_end].rfind("[")
    try:
        while token_start > 0 and s[token_start-1].isdigit():
            token_start -= 1
    except IndexError:
        pass
    return token_start, s[token_start:token_end+1]


class Solution:
    def __init__(self):
        pass

    def decodeString(self, s: str) -> str:
        _workstring = copy(s)
        idx = _workstring.find("]")
        while idx > 0:
            idx, token = extracttoken(_workstring)
            res = expandtoken(token)
            _workstring = reassemble(_workstring, res, idx, idx+len(token))
            idx = _workstring.find("]")  # continue until no more tokens left
        return _workstring


if __name__ == "__main__":
    inputstr = "leetcode"
    sol = Solution()
    print(f'Init string: {inputstr}')
    print("result:", sol.decodeString(inputstr))