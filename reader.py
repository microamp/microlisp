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


def read_str(s):
    """Read the input string tokenised.
    """
    reader = (token for token in tokeniser(s))
    return read_form(reader)


def tokeniser(s):
    """Tokenise the input string using PCRE (Perl Compatible Regular
    Expression).

    [\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]*)"""
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
    """Read a list/atom."""
    token = next(reader)
    return read_list(reader) if is_list(token) else read_atom(token)


def read_seq(reader, end_char=LIST_END):
    tokens, token = [], read_form(reader)
    while not (isinstance(token, Symbol) and token == end_char):
        tokens.append(token)
        token = read_form(reader)

    return LinkedList.build(*tokens)


def read_list(reader):
    return read_seq(reader, end_char=LIST_END)


def read_atom(token):
    if is_bool(token):
        return Bool(True if token == "true" else False)
    elif is_int(token):
        return Int(token)
    elif is_nil(token):
        return Nil()
    elif is_str(token):
        return Str(token.strip('"'))
    else:
        return Symbol(token)


if __name__ == "__main__":
    tokens = tokeniser("( + 2 (* 3 4) )")
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
