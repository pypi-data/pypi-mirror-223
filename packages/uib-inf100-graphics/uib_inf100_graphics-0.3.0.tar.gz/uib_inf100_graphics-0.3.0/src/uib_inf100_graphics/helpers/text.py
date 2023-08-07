from tkinter import Canvas
from tkinter.font import Font, nametofont
from tkinter import TclError
from typing import Literal, Callable

from uib_inf100_graphics.helpers.logger import _warning


AnchorType = Literal['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'center']

def text_in_box(
            canvas: Canvas,
            x1: float, y1: float, x2: float, y2: float,
            text: str,
            font: str|Font|tuple[str, int, str]|None=None,
            fit_mode: Literal['contain', 'fill', 'height', 'width']='contain',
            padding: float=0,
            min_font_size: int=1,
            justify: Literal['left', 'center', 'right']='center',
            align: Literal['top', 'center', 'bottom']='center',
            **kwargs):
    """
    Draws text into a rectangle, scaling it to fit the rectangle. The text will
    be centered at the center of the rectangle. The minium font size of the
    text will be 1, so if the rectangle is too small, the text may overflow
    with font size 1.

    
    Positional parameters
    ----------
    canvas : Canvas
        The canvas to draw on.
    x1 : float
        The x-coordinate of the top-left corner of the bounding box.
    y1 : float 
        The y-coordinate of the top-left corner of the bounding box.
    x2 : float
        The x-coordinate of the bottom-right corner of the bounding box.
    y2 : float
        The y-coordinate of the bottom-right corner of the bounding box.
    text : str
        The text to draw.

    Optional parameters
    ----------
    font : str|Font|tuple[str, int, str]|None, optional
        The font to use. If None or unspecified the default font will be
        used. The font may be specified as 
          - a string with the name of the font family or a named font for
            example "TkFixedFont", or "Times new roman"; or
          - a font specifier tuple, for example
            ("Times new roman", 12, "bold") or ("Courier", 14, "italic"); or
          - a tkinter.font.Font object.

        Note that the size of the font will be ignored (the actual font size
        used will instead be calculated). However, it is still necessary to
        specify some value for the font size when the font is specified with
        a font specifier tuple. If the font is not found, the default
        font will be used.

    fit_mode : Literal['contain', 'fill', 'height', 'width'], optional
        The mode to use for fitting the text into the rectangle. If 'contain',
        the text will be scaled to fit entirely within the rectangle (default).
        If 'fill', the text will be scaled to fill the rectangle, and may
        overflow in either width or height (but not both). If 'height', the
        text will be scaled to fit the height of the rectangle (the width
        of the rectangle will be ignored). If 'width', the text will be scaled
        to fit the width of the rectangle (the height of the rectangle will be
        ignored).
    padding : float, optional
        The padding to leave around the text relative to the bounding box.
        Defaults to 0. The padding is the same on all sides of the box.
    min_font_size : int, optional
        The minimum font size to use. Defaults to 1. Must be at least 1.
    justify : Literal['left', 'center', 'right'], optional
        The horizontal justification of the text. Defaults to 'center'.
    align : Literal['top', 'center', 'bottom'], optional
        The vertical alignment of the text. Defaults to 'center'.
    **kwargs
        Additional keyword arguments to pass to the canvas.create_text method.

    Returns
    -------
    int
        The id of the text object created.

    Raises
    ------
    ValueError
        If fit_mode is not one of 'contain', 'fill', 'height', or 'width',
        or if justify is not one of 'left', 'center', or 'right', or if
        align is not one of 'top', 'center', or 'bottom', or if
        min_font_size is not a positive integer
    """
    # Validate arguments
    if fit_mode not in ['contain', 'fill', 'height', 'width']:
        raise ValueError("fit_mode must be one of 'contain', 'fill', 'height',"
                         + f" or 'width', but got '{fit_mode}'")
    if justify not in ['left', 'center', 'right']:
        raise ValueError("justify must be one of 'left', 'center', or 'right',"
                         + f" but got '{justify}'")
    if align not in ['top', 'center', 'bottom']:
        raise ValueError("align must be one of 'top', 'center', or 'bottom',"
                         + f" but got '{align}'")
    if min_font_size < 1:
        raise ValueError(f"min_font_size must >= 1, but got {min_font_size}")

    # Clean up kwargs
    if "anchor" in kwargs:
        del kwargs["anchor"]

    # Get the font
    font = _get_font(font)

    # Calculate the font size based on longest line and number of lines total
    number_of_lines = text.count("\n") + 1
    longest_line = max(text.split("\n"), key=len)
    if len(longest_line) <= 0:
        return # Nothing to draw
    max_width = max(0, abs(x2 - x1) - 2*padding)
    max_height = max(0, abs(y2 - y1) - 2*padding)/number_of_lines
    fontsize = _get_fontsize(longest_line, font, max_width, max_height,
                            fit_mode, min_font_size)
    font.configure(size=fontsize)

    # Calculate the position and create the text
    x, y, anchor = _get_text_position(x1, y1, x2, y2, justify, align, padding)
    return canvas.create_text(x, y, text=text, font=font, anchor=anchor,
                              justify=justify, **kwargs)


def _get_text_position(x1: float, y1: float, x2: float, y2: float,
                       justify: Literal['left', 'center', 'right'],
                       align: Literal['top', 'center', 'bottom'],
                       padding: float) -> tuple[float, float, AnchorType]:
    """Calculate the position of the text and the anchor to use."""
    anchor: AnchorType = "center"
    y: float = (y1 + y2)/2
    x: float
    if justify == "center":
        anchor = "center"
        x = (x1 + x2)/2
    elif justify == "left":
        anchor = "w"
        x = min(x1, x2) + padding
    elif justify == "right":
        anchor = "e"
        x = max(x1, x2) - padding

    if align == "top":
        anchor = "n" + anchor if anchor != "center" else "n"
        y = min(y1, y2) + padding
    elif align == "bottom":
        anchor = "s" + anchor if anchor != "center" else "s"
        y = max(y1, y2) - padding
    return x, y, anchor


def _get_fontsize(text: str, font: Font, max_width: float, max_height: float,
                 fit_mode: Literal['contain', 'fill', 'height', 'width'],
                 min_font_size: int) -> int:
    """Calculate the font size to use for the text."""
    if fit_mode == 'contain':
        return min(_fontsize_fit_height(max_height, font, min_font_size),
                   _fontsize_fit_width(max_width, font, text, min_font_size))
    elif fit_mode == 'fill':
        return max(_fontsize_fit_height(max_height, font, min_font_size),
                   _fontsize_fit_width(max_width, font, text, min_font_size))
    elif fit_mode == 'height':
        return _fontsize_fit_height(max_height, font, min_font_size)
    elif fit_mode == 'width':
        return _fontsize_fit_width(max_width, font, text, min_font_size)
    else:
        raise ValueError(f"Unknown fit_mode '{fit_mode}'")


def _get_font(font_spec: str|Font|tuple[str, int, str]|None) -> Font:
    """Get a font object from a font specification."""
    if isinstance(font_spec, Font):
        return font_spec
    if isinstance(font_spec, str):
        try:
            return nametofont(font_spec).copy()
        except TclError:
            pass
        try:
            return string_to_font(font_spec)
        except (ValueError, TclError):
            pass
        try:
            f = Font(family=font_spec)
            if font_spec.lower() == f.actual()['family'].lower():
                return f
            raise TclError()
        except TclError:
            pass
        _warning(f"Could not create font from string '{font_spec}',"
                 + " will use default font instead")
    elif isinstance(font_spec, tuple):
        try:
            return Font(font=font_spec)
        except TclError:
            pass
        _warning(f"Could not create font from tuple '{font_spec}',"
                 + " will use default font instead")
    # If we get here, we'll just use the default font
    return nametofont('TkDefaultFont').copy()


def string_to_font(s: str) -> Font:
    """
    Convert a font string to a Font object. The string must be in the
    format 'family size [weight] [slant] [underline] [overstrike]', where
    'family' is the font family, 'size' is the font size in points, 'weight'
    is either 'bold' or 'normal', 'slant' is either 'italic' or 'roman',
    'underline' is either 'underline' or 'normal', and 'overstrike' is either
    'overstrike' or 'normal'. The font family and size are required, the rest
    are optional. If the font string is not valid, a ValueError is raised.
    """
    parts = s.split()

    size_index = next((i for i, part in enumerate(parts) if part.isdigit()), None)
    if size_index is None:
        raise ValueError(f'Not a valid font string: {s:r}')

    family = ' '.join(parts[:size_index])
    size = int(parts[size_index])
    options = [part.lower() for part in parts[size_index+1:]]

    weight = 'bold' if 'bold' in options else 'normal'
    slant = 'italic' if 'italic' in options else 'roman'
    underline = 'underline' in options
    overstrike = 'overstrike' in options

    return Font(family=family, size=size, weight=weight, 
                       slant=slant, underline=underline, overstrike=overstrike)


def _fontsize_fit_height(max_height: float, font: Font,
                         min_value: int) -> int:
    """
    Find the largest font size that fits within the given height.
    """
    def get_height(fontsize: int) -> float:
        font.configure(size=fontsize)
        return font.metrics("linespace")
    return _binary_search_maximize_int_outcome_below(max_height, get_height,
                                                     min_value)

def _fontsize_fit_width(max_width: float, font: Font, text: str,
                        min_value: int) -> int:
    """
    Find the largest font size that fits within the given width
    for the given text. The text is assumed to be a single line.
    """
    def get_width(fontsize: int) -> float:
        font.configure(size=fontsize)
        return font.measure(text)
    return _binary_search_maximize_int_outcome_below(max_width, get_width,
                                                     min_value)

def _binary_search_maximize_int_outcome_below(threshold: float,
                             measure: Callable[[int], float],
                             min_value: int=0) -> int:
    """
    Find the largest integer value that is less than or equal to the
    threshold for the given measure function. The measure function
    should take an integer argument and return a float. The measure
    function should be monotonically increasing with respect to the
    integer argument.
    """
    hi: int = max(1, min_value + 1)
    while measure(hi) <= threshold:
        hi *= 2
    lo: int = min_value if hi == 1 else max(min_value, hi // 2)
    return _binary_search(lambda x: measure(x) <= threshold, hi, lo)

def _binary_search(predicate: Callable[[int], bool],
                   impossible_value: int,
                   possible_value: int) -> int:
    """
    Find an integer value that satisfies the given predicate which is
    neighbouring an integer which does not. For example, consider the
    monotonic sequence of all integers in the range between
    possible_value and impossible_value, starting with the
    possible_value. If the predicate is True for the first few
    integers, and then is False for the rest, this function will return
    the latest integer in the sequence for which the predicate is True.

    It is assumed that the predicate is monotonic with respect to the
    integer argument. That is, there is at most one integer x in the
    range for which the predicate yields a different answer for x and
    x+1. If the predicate is not monotonic, the behaviour of this
    function is undefined.

    The impossible_value should be an integer which does not satisfy
    the predicate, and the possible_value is some integer which does;
    however if the impossible_value actually does satisfy the
    predicate, it will be returned -- similarly, if the possible_value
    does NOT satisfy the predicate, it will be returned. If both these
    conditions are true, the behaviour of this function is undefined.
    """
    while (abs(possible_value - impossible_value) > 1):
        mid = (impossible_value + possible_value) // 2
        if predicate(mid):
            possible_value = mid
        else:
            impossible_value = mid
    return possible_value