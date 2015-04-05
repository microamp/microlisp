# -*- coding: utf-8 -*-

import operator
from functools import reduce
from collections import Iterable

from datatypes import Bool, Int, Str, LinkedList
from reader import read_str
from printer import print_str


def variadic(fn):
    def _variadic(*args):
        return Int(reduce(fn(), args if isinstance(args, Iterable) else ()))

    return _variadic


def predicate(fn):
    def _predicate(x, y):
        return Bool(fn()(x, y))

    return _predicate


@variadic
def add(*args):
    return operator.add


@variadic
def sub(*args):
    return operator.sub


@variadic
def mul(*args):
    return operator.mul


@variadic
def truediv(*args):
    return operator.truediv


@predicate
def eq(*args):
    return operator.eq


@predicate
def lt(*args):
    return operator.lt


@predicate
def le(*args):
    return operator.le


@predicate
def gt(*args):
    return operator.gt


@predicate
def ge(*args):
    return operator.ge


def read_file(filename, *args):
    with open(filename) as f:
        return Str(f.read().strip())


def strfy(*strs):
    invalid = list(filter(lambda s: not isinstance(s, Str), strs))
    assert not invalid, ("invalid parameters: {0}"
                         "".format(", ".join(map(str, invalid))))
    return Str(reduce(lambda s1, s2: operator.add(s1, s2), strs))


# symbol-to-function mappings
ns = {"+": add,
      "-": sub,
      "*": mul,
      "/": truediv,
      "=": eq,
      "<": lt,
      "<=": le,
      ">": gt,
      ">=": ge,
      "car": lambda ll: ll.car(),
      "cdr": lambda ll: ll.cdr(),
      "concat": lambda *lls: reduce(lambda l1, l2: l1.concat(l2), lls),
      "cons": lambda item, ll: ll.cons(item),
      "count": lambda ll, *args: len(ll),
      "empty?": lambda ll, *args: Bool(len(ll) == 0),
      "list": lambda *args: LinkedList.build(*args),
      "list?": lambda ll, *args: Bool(isinstance(ll, LinkedList)),
      "print": print_str,
      "prn": print_str,
      "read-string": read_str,
      "reverse": lambda ll: ll.reverse(),
      "slurp": read_file,
      "str": strfy,
      "type": type}
