import typing

X = typing.TypeVar("X")


def p(prop: typing.Union[typing.Callable[[...], X], X]) -> X:
    """
    Silly little type cast for things that are actually properties
    that PyCharm doesn't recognize are properties
    """
    return typing.cast(X, prop)
