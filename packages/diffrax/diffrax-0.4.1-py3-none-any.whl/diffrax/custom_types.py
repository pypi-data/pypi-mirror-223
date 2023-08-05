import inspect
import typing
from typing import Any, Dict, Generic, Tuple, TypeVar, Union

import equinox.internal as eqxi
import jax.tree_util as jtu


# Custom flag we set when generating documentation.
# We do a lot of custom hackery in here to produce nice-looking docs.
if getattr(typing, "GENERATING_DOCUMENTATION", False):

    def _item_to_str(item: Union[str, type, slice]) -> str:
        if isinstance(item, slice):
            if item.step is not None:
                raise NotImplementedError
            return _item_to_str(item.start) + ": " + _item_to_str(item.stop)
        elif item is ...:
            return "..."
        elif inspect.isclass(item):
            return item.__name__
        else:
            return repr(item)

    def _maybe_tuple_to_str(
        item: Union[str, type, slice, Tuple[Union[str, type, slice], ...]]
    ) -> str:
        if isinstance(item, tuple):
            if len(item) == 0:
                # Explicit brackets
                return "()"
            else:
                # No brackets
                return ", ".join([_item_to_str(i) for i in item])
        else:
            return _item_to_str(item)

    #
    # First we have custom versions of Array and PyTree, that the usual Array and
    # PyTree are just syntactic sugar around.
    #
    # Crucially the __module__ and __qualname__ are overridden. This particular combo
    # makes Python's typing module just use the __qualname__ as what is displayed in
    # stringified type annotations.
    # (Which for some strange reason are neither str(...) or repr(...) but some other
    # custom thing.)
    #
    # c.f.
    # https://github.com/python/cpython/blob/634984d7dbdd91e0a51a793eed4d870e139ae1e0/Lib/typing.py#L203  # noqa: E501
    #
    # Note that in general overriding __module__ can be a bit dangerous, and will break
    # functionality in the inspect standard library.
    #

    _Annotation = TypeVar("_Annotation")

    class _Array(Generic[_Annotation]):
        pass

    class _PyTree(Generic[_Annotation]):
        pass

    _Array.__module__ = "builtins"
    _Array.__qualname__ = "Array"
    _PyTree.__module__ = "builtins"
    _PyTree.__qualname__ = "PyTree"

    #
    # Now we have Array and PyTree themselves. In order to get the desired behaviour in
    # docs, we now pass in a type variable with the right __qualname__ (and __module__
    # set to "builtins" as usual) that will render in the desired way.
    #

    class Array:
        def __class_getitem__(cls, item):
            class X:
                pass

            X.__module__ = "builtins"
            X.__qualname__ = _maybe_tuple_to_str(item)
            return _Array[X]

    class PyTree:
        def __class_getitem__(cls, item):
            class X:
                pass

            X.__module__ = "builtins"
            X.__qualname__ = _maybe_tuple_to_str(item)
            return _PyTree[X]

    # Same __module__ trick here again. (So that we get the correct display when
    # doing `def f(x: Array)` as well as `def f(x: Array["dim"])`.
    #
    # Don't need to set __qualname__ as that's already correct.
    Array.__module__ = "builtins"
    PyTree.__module__ = "builtins"

    # Represent Scalar as a non-Union type in docs.
    class Scalar:
        pass

    Scalar.__module__ = "builtins"  # once again __qualname__ is already good.

    # Skip the union with Array in docs.
    Int = int
    Bool = bool

    #
    # Because they appear in our docstrings, we also monkey-patch some non-Diffrax
    # types that have similar defined-in-one-place, exported-in-another behaviour.
    #

    jtu.Partial.__module__ = "jax.tree_util"

else:

    class Array:
        def __class_getitem__(cls, item):
            return Array

    class PyTree:
        def __class_getitem__(cls, item):
            return PyTree

    Scalar = Union[int, float, Array[()]]

    Int = Union[int, Array[(), int]]
    Bool = Union[bool, Array[(), bool]]

DenseInfo = Dict[str, PyTree[Array]]
DenseInfos = Dict[str, PyTree[Array["times", ...]]]  # noqa: F821
sentinel: Any = eqxi.doc_repr(object(), "sentinel")
