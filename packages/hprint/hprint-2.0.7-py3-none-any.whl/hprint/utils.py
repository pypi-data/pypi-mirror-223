from functools import partial


def install_print_with_flush():
    try:
        builtins = __import__('__builtin__')
    except ImportError:
        builtins = __import__('builtins')

    setattr(builtins, 'print0', print)
    setattr(builtins, 'print', partial(print, flush=True))
