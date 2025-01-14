#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2021, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
''' Text related models
'''

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import annotations

import logging # isort:skip
log = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Bokeh imports
from ..core.has_props import abstract
from ..core.properties import (
    Dict,
    Either,
    Int,
    NonNullable,
    String,
    Tuple,
)
from ..model import Model

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    "Ascii",
    "MathML",
    "MathText",
    "PlainText",
    "TeX",
)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

@abstract
class BaseText(Model):
    """
    Base class for renderers of text content of various kinds.
    """

    def __init__(self, *args, **kwargs) -> None:
        if len(args) == 1 and "text" not in kwargs:
            kwargs["text"] = args[0]

        super().__init__(**kwargs)

    text = NonNullable(String, help="""
    The text value to render.
    """)

@abstract
class MathText(BaseText):
    """
    Base class for renderers of mathematical content.
    """

class Ascii(MathText):
    """
    Render mathematical content using `AsciiMath <http://asciimath.org/>` notation.
    """

class MathML(MathText):
    """
    Render mathematical content using `MathML <https://www.w3.org/Math/>` notation.
    """

class TeX(MathText):
    """
    Render mathematical content using `LaTeX <https://www.latex-project.org/>`_
    notation.

    .. note::
        Bokeh uses `MathJax <https://www.mathjax.org>`_ to render text
        containing mathematical notation.

        MathJax only supports math-mode macros (no text-mode macros). You
        can see more about differences between standard TeX/LaTeX and MathJax
        here: https://docs.mathjax.org/en/latest/input/tex/differences.html
    """

    macros = Dict(String, Either(String, Tuple(String, Int)), help="""
    User defined TeX macros.

    This is a mapping from control sequence names (without leading backslash) to
    either replacement strings or tuples of a replacement string and a number
    of arguments.

    Example:

    .. code-block:: python

        TeX(text=r"\\R \\rightarrow \\R^2", macros={"RR": r"{\\bf R}"})

    """)

class PlainText(BaseText):
    """
    Represents plain text in contexts where text parsing is allowed.
    """

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
