# -*- coding: utf-8 -*-

import collections
from functools import reduce


class Bool(int):
    def __str__(self):
        return "true" if self == 1 else "false"


class Int(int):
    pass


class Nil(object):
    """TODO: can we do this better here?
    """
    def __str__(self):
        return "nil"

    def __eq__(self, other):
        return isinstance(other, Nil)


class Str(str):
    pass


class Symbol(str):
    pass


class LinkedList(collections.namedtuple("LinkedList", ("head", "tail",))):
    """Implementation of (immutable) singly linked list.
    """

    @staticmethod
    def build(*items):
        def _build():
            r = list(reversed(items))
            return reduce(lambda ll, x: ll.cons(x),
                          r[1:],
                          LinkedList(head=r[0], tail=None))

        return _build() if items else LinkedList(head=None, tail=None)

    def __iter__(self):
        ll = self
        while ll is not None and ll.head is not None:
            yield ll.head
            ll = ll.tail

    def __len__(self):
        return sum(1 for _ in iter(self))

    def __str__(self):
        return "({0})".format(" ".join(map(str, iter(self))))

    def car(self):
        return self.head

    def cdr(self):
        return self.tail

    def cons(self, item):
        return LinkedList(head=item, tail=self)

    def reverse(self):
        return reduce(lambda ll, x: ll.cons(x),
                      self.cdr(),
                      LinkedList(head=self.car(), tail=None))

    def concat(self, other):
        r = self.reverse()
        return reduce(lambda ll, x: ll.cons(x),
                      r.cdr(),
                      other.cons(r.car()))

    hd = first = car  # aliases of `car`
    tl = rest = cdr  # aliases of `cdr`


if __name__ == "__main__":
    # TODO: move the below to seprate tests

    # Symbol
    x = Symbol("x")
    assert x == "x"
    assert x != "y"

    # Int
    ten = Int(10)
    assert ten == 10
    assert ten != 100

    # Bool
    true = Bool(True)
    assert true == Bool(True)
    assert true != Bool(False)

    # Nil
    nil = Nil()
    assert nil == Nil()

    # Str
    s1 = Str("hello")
    assert s1 == "hello"
    s2 = Str("world")
    assert s2 == "world"
    assert s1 + " " + s2 == "hello world"

    # LinkedList
    ll_one = LinkedList(head=1, tail=None)
    assert ll_one.car() == 1
    assert ll_one.cdr() is None
    assert tuple(iter(ll_one)) == (1,)
    assert len(ll_one) == 1

    ll_two = LinkedList.build(1, 2, 3)
    assert ll_two.car() == 1
    assert tuple(iter(ll_two.cdr())) == (2, 3,)
    assert len(ll_two) == 3

    consed = ll_two.cons(0)
    assert consed.car() == 0
    assert tuple(iter(consed.cdr())) == (1, 2, 3,)
    assert str(consed) == "(0 1 2 3)"
    assert len(consed) == 4

    empty = LinkedList(head=None, tail=None)
    assert empty.car() is None
    assert empty.cdr() is None
    assert str(empty) == "()"
    assert len(empty) == 0
