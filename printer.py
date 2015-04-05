# -*- coding: utf-8 -*-

import types

from datatypes import Str


# TODO: better name than '#function'
printers = {Str: lambda data: '"{0}"'.format(data),
            types.FunctionType: lambda data: "#function"}
default_printer = lambda data: str(data)


def print_str(data, print_readably=True):
    strfied = printers.get(type(data), default_printer)(data)

    try:
        return strfied
    finally:
        if print_readably:
            print(strfied)
