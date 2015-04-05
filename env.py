# -*- coding: utf-8 -*-

from errors import NoSymbolFound


class Env(object):
    def __init__(self, outer=None, binds=(), exprs=()):
        self.outer = outer
        self.data = {}
        assert len(binds) == len(exprs), "binds and expressions mismatch"
        for index in range(len(binds)):
            self.set(binds[index], exprs[index])

    def __str__(self):
        return str(self.data)

    def set(self, key, value):
        self.data.update({str(key): value})

    def find(self, key):
        if str(key) in self.data:
            return self
        elif self.outer is not None:
            return self.outer.find(str(key))
        else:
            return None

    def get(self, key):
        env = self.find(str(key))
        if env and str(key) in env.data:
            return env.data[str(key)]
        else:
            raise NoSymbolFound("no such symbol: '{0}'".format(key))


if __name__ == "__main__":
    env = Env(None)
    env.set("x", 10)
    assert env.get("x") == 10
