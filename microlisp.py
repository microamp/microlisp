# -*- coding: utf-8 -*-

import functools

import reader
import printer
import lib
from datatypes import Nil, Bool, Symbol, LinkedList
from env import Env
from core import ns, concat
from errors import NoEnvFound, NoSpecialFormFound

# special forms (TODO: special forms)
SF_DEF = "def!"
SF_DO = "do"
SF_FN = "fn*"
SF_IF = "if"
SF_LET = "let*"
SF_QUASIQUOTE = "quasiquote"
SF_QUASIQUOTE_2 = "`"
SF_QUOTE = "quote"
SF_QUOTE_2 = "'"
SF_SPLICE_UNQUOTE = "splice-unquote"
SF_SPLICE_UNQUOTE_2 = "~@"
SF_UNQUOTE = "unquote"
SF_UNQUOTE_2 = "~"
SPECIAL_FORMS = {SF_DEF,
                 SF_DO,
                 SF_FN,
                 SF_IF,
                 SF_LET,
                 SF_QUASIQUOTE,
                 SF_QUOTE}

# symbols
SYMBOL_EVAL = "eval"


def READ(s):
    return reader.read_str(s)


def _sf_def(ast, env):
    """Evaluate the special form, `def!`.
    """
    k, v = ast.cdr()
    evaled = EVAL(v, env=env)  # key inevaluated, value evaluted
    env.set(k, evaled)
    return evaled


def _sf_do(ast, env):
    """Evaluate the special form, `do`.
    """
    body = ast.cdr()
    return [EVAL(ast_, env=env) for ast_ in body][-1]


def _sf_fn(ast, env):
    """Evaluate the special form, `fn*`. Return a new function closure.
    """
    def closure(*exprs):
        binds, expr = ast.cdr()
        inner_env = Env(outer=env,
                        binds=binds,
                        exprs=tuple(EVAL(e, env=env) for e in exprs))
        return EVAL(expr, env=inner_env)

    return closure


def _sf_if(ast, env):
    """Evaluate the special form, `if`.
    """
    def _is_true(value):
        return value not in (Nil(), Bool(False),)

    body = ast.cdr()
    assert len(body) in (2, 3,), "body of `if` requires at least two forms"

    expr2 = Nil()  # nil by default
    if len(body) == 2:
        pred, expr1 = body
    else:
        pred, expr1, expr2 = body

    return (EVAL(expr1, env=env) if _is_true(EVAL(pred, env=env)) else
            EVAL(expr2, env=env))


def _sf_let(ast, env):
    """Evaluate the special form, `let*`.
    """
    def _build_let_pairs(items):
        assert len(items) % 2 == 0, "body of `let` must be in pairs"
        return ((items[index], items[index + 1])
                for index in range(0, len(items), 2))

    bindings, expr = ast.cdr()
    binds, exprs = zip(*_build_let_pairs(list(bindings)))
    inner_env = Env(outer=env,
                    binds=binds,
                    exprs=tuple(EVAL(e, env=env) for e in exprs))
    return EVAL(expr, env=inner_env)


def _sf_quasiquote(ast, env):
    """Evaluate the special form, `quasiquote`.
    """
    def _unquote(ast):
        if isinstance(ast, LinkedList):
            sf, body = ast.car(), ast.second()
            evaled = EVAL(body, env=env)
            if sf in (SF_UNQUOTE,):
                return LinkedList.build(evaled)
            elif sf in (SF_SPLICE_UNQUOTE,):
                return evaled
        return LinkedList.build(ast)

    return concat(*[_unquote(form) for form in ast.second()])


def _sf_quote(ast, env):
    """Evaluate the special form, `quote`.
    """
    return ast.second()


special_form_fns = {SF_DEF: _sf_def,
                    SF_DO: _sf_do,
                    SF_FN: _sf_fn,
                    SF_IF: _sf_if,
                    SF_LET: _sf_let,
                    SF_QUASIQUOTE: _sf_quasiquote,
                    SF_QUOTE: _sf_quote}
assert SPECIAL_FORMS == special_form_fns.keys()


def apply(ast, env):
    hd = ast.car()
    if hd in SPECIAL_FORMS:
        sf = special_form_fns.get(hd)
        assert sf is not None, NoSpecialFormFound("no special form found: "
                                                  "'{0}'".format(hd))
        return sf(ast, env)
    else:  # normal function call
        new_list = eval_ast(ast, env)
        fn, args = new_list.car(), new_list.cdr()
        return fn(*iter(args)) if args is not None else fn()


def eval_ast(ast, env):
    if isinstance(ast, LinkedList):  # list
        return LinkedList.build(*tuple(EVAL(symbol, env=env)
                                       for symbol in ast))
    elif isinstance(ast, Symbol):  # symbol
        return env.get(ast)  # symbol lookup
    else:
        return ast


def EVAL(ast, env=None):
    assert env is not None, NoEnvFound("environment must exist")
    if isinstance(ast, LinkedList):  # list
        return apply(ast, env)
    else:  # symbol
        return eval_ast(ast, env)


def PRINT(ast, print_readably=True):
    return printer.print_str(ast, print_readably=print_readably)


def rep(s, env):
    # read -> eval -> print
    loop = lib.compose(READ,
                       functools.partial(EVAL, env=env),
                       PRINT)
    return loop(s)


def repl():
    # set up base environment
    env = Env(outer=None)
    for k, v in ns.items():
        env.set(k, v)

    env.set(SYMBOL_EVAL, lambda ast: EVAL(ast, env=env))  # `eval` added to ns

    s = """
    (def! load-file
      (fn* (f)
        (eval (read-string (str "(do " (slurp f) ")")))))
    """
    EVAL(READ(s), env=env)

    # read-eval-print loop
    while True:
        try:
            s = input("=> ")
            rep(s, env)
        except Exception as e:
            print("error: {0}".format(e))


if __name__ == "__main__":
    repl()
