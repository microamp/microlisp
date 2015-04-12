# -*- coding: utf-8 -*-

import functools


def compose(*fns):
    """Compose functions."""
    def _compose(*args, **kwargs):
        return functools.reduce(lambda v, g: g(v),
                                fns[1:],
                                fns[0](*args, **kwargs))

    return _compose
