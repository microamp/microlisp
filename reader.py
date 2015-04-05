# -*- coding: utf-8 -*-

import re

from datatypes import Bool, Int, Nil, Str, Symbol, LinkedList

TOKEN_PATTERN = (
    r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]*)"""
)
LIST_START, LIST_END = "(", ")"
STRING_START, STRING_END = '"', '"'
COLON = ":"

token_pattern = re.compile(TOKEN_PATTERN)


class Reader(object):
    """This object will store the tokens and a position. The Reader object will
    have two methods: next and peek. next returns the tokens at the current
    position and increments the position. peek just returns the token at the
    current position.
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def next(self):
        token = self.tokens[self.position]
        self.position += 1
        return token

    def peek(self):
        return self.tokens[self.position]


def read_str(s):
    """Call tokenizer and then create a new Reader object instance with the
    tokens. Then it will call read_form with the reader instance.
    """
    tokens = tokenizer(s)
    reader = Reader(tokens)
    return read_form(reader)


def tokenizer(s):
    """Take a single string and return an array/list of all the tokens
    (strings) in it. The following regular expression (PCRE) will match all
    tokens.

    [\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]*)
    """
    return [token for token in token_pattern.findall(s) if token]


def is_bool(token):
    return token in ("true", "false",)


def is_int(token):
    return token.isdigit()


def is_nil(token):
    return token == "nil"


def is_str(token):
    return (token.startswith(STRING_START) and
            token.endswith(STRING_END) and
            token.count('"') == 2)


def is_list(token):
    return token and token[0] == LIST_START


def read_form(reader):
    """Peek at the first token in the Reader object and switch on the first
    character of that token. If the character is a left paren then read_list is
    called with the Reader object. Otherwise, read_atom is called with the
    Reader Object.
    """
    token = reader.next()
    return read_list(reader) if is_list(token) else read_atom(token)


def read_seq(reader, end_char=LIST_END):
    tokens, token = [], read_form(reader)
    while not (isinstance(token, Symbol) and token == end_char):
        tokens.append(token)
        token = read_form(reader)

    return LinkedList.build(*tokens)


def read_list(reader):
    """Repeatedly call read_form with the Reader object until it encounters a
    ')' token. Accumulates the results into a List type.
    """
    return read_seq(reader, end_char=LIST_END)


def read_atom(token):
    """Look at the contents of the token and return the appropriate scalar
    (simple/single) data type value.
    """
    if is_int(token):
        return Int(token)
    elif is_bool(token):
        return Bool(True if token == "true" else False)
    elif is_nil(token):
        return Nil()
    elif is_str(token):
        return Str(token.strip('"'))
    else:
        return Symbol(token)


if __name__ == "__main__":
    tokens = tokenizer("( + 2 (* 3 4) )")
    assert tokens == ["(", "+", "2", "(", "*", "3", "4", ")", ")"]

    # int
    ast = read_str("123")
    assert isinstance(ast, Int)
    assert str(ast) == "123"

    # str
    ast = read_str('"abc"')
    assert isinstance(ast, Str)
    assert ast == "abc"  # no quotes!

    # symbol
    ast = read_str("+")
    assert isinstance(ast, Symbol)
    assert str(ast) == "+"

    # linked list
    ast = read_str("(+ 1 2)")
    assert isinstance(ast, LinkedList)
    assert str(ast) == "(+ 1 2)"

    ast = read_str("( + 2 (* 3 4) )")
    assert isinstance(ast, LinkedList)
    assert str(ast) == "(+ 2 (* 3 4))"
