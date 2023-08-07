import sys
from tkinter import Canvas, ALL, Tk
from typing import Any, Final

from PIL import Image, ImageTk


class RecordingCanvas(Canvas):
    """
    A SimplifiedCanvas object gives the illusion of being a regular
    Tk.Canvas object from tkinter, by having all the create_ -methods
    available; but it is actually an empty wrapper which simply records
    all the calls made to it.

    Note that unlike the functions in a proper Tk.Canvas object, the
    create_ -methods in this class only return a fake id. The id is not
    used for anything, and is assigned in increasing order starting from
    1 in the order in which the calls are made.
    """

    def __init__(self, root: Tk):
        self._calls: Final[list[tuple[int, str, tuple[Any], dict[str, Any]]]] = []
        super().__init__(root)
        self._is_disabled: bool = False
        self._tkroot: Final[Tk] = root

    def _get_calls(self) -> tuple[tuple[int, str, tuple[Any], dict[str, Any]]]:
        return tuple(self._calls)
    
    def _clear(self) -> None:
        super().delete(ALL)
        self._calls.clear()

    def _disable(self) -> None:
        self._is_disabled = True

    def _verify_enabled(self) -> None:
        # If root is destroyed, we should exit the program
        # (otherwise it will hang forever)
        # TODO: This is a hack, should probably be fixed in a better way
        if "_is_destroyed" in self._tkroot.__dict__ and self._tkroot.__dict__["_is_destroyed"]:
            sys.exit(0)

    def create_arc(self, *args: Any, **kwargs: Any) -> int:
        """
        Create arc shaped region with coordinates x1,y1,x2,y2.

        For a complete documentation, read the official
        tkinter documentation on the create_arc method:
        https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html#Canvas.create_arc
        """
        self._verify_enabled()
        idnum: int = super().create_arc(*args, **kwargs)
        self._calls.append((idnum, "create_arc", args, kwargs))
        return idnum

    def create_bitmap(self, *args: Any, **kwargs: Any) -> int:
        """
        Create bitmap with coordinates x1,y1.

        For a complete documentation, read the official
        tkinter documentation on the create_bitmap method:
        https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html#Canvas.create_bitmap
        """
        self._verify_enabled()
        idnum: int = super().create_bitmap(*args, **kwargs)
        self._calls.append((idnum, "create_bitmap", args, kwargs))
        return idnum

    def create_image(self, *args: Any, **kwargs: Any) -> int:
        """
        Create image with coordinates x1,y1. To show an image, use the pil_image named argument
        to provide a PIL.Image object (this differs slightly from the tkinter version).

        For example:
        ```
        from uib_inf100_graphics.simple import canvas, display
        from uib_inf100_graphics.imagetools import load_image

        image = load_image('https://tinyurl.com/inf100kitten-png')
        canvas.create_image(200, 200, pil_image=image)
        display(canvas)
        ```
        
        For a complete documentation, read the official
        tkinter documentation on the create_image method:
        https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html#Canvas.create_image
        """
        self._verify_enabled()
        _pil_to_photoimage(kwargs)
        idnum: int = super().create_image(*args, **kwargs)
        self._calls.append((idnum, "create_image", args, kwargs))
        return idnum

    def create_line(self, *args: Any, **kwargs: Any) -> int:
        """
        Create line with coordinates x1,y1,...,xn,yn.
        
        For a complete documentation, read the official
        tkinter documentation on the create_line method:
        https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html#Canvas.create_line
        """
        self._verify_enabled()
        idnum: int = super().create_line(*args, **kwargs)
        self._calls.append((idnum, "create_line", args, kwargs))
        return idnum

    def create_oval(self, *args: Any, **kwargs: Any) -> int:
        """
        Create oval with coordinates x1,y1,x2,y2.
        
        For a complete documentation, read the official
        tkinter documentation on the create_oval method:
        https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html#Canvas.create_oval
        """
        self._verify_enabled()
        idnum: int = super().create_oval(*args, **kwargs)
        self._calls.append((idnum, "create_oval", args, kwargs))
        return idnum

    def create_polygon(self, *args: Any, **kwargs: Any) -> int:
        """
        Create polygon with coordinates x1,y1,...,xn,yn.

        For a complete documentation, read the official
        tkinter documentation on the create_polygon method:
        https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html#Canvas.create_polygon
        """
        self._verify_enabled()
        idnum: int = super().create_polygon(*args, **kwargs)
        self._calls.append((idnum, "create_polygon", args, kwargs))
        return idnum

    def create_rectangle(self, *args: Any, **kwargs: Any) -> int:
        """
        Create rectangle with coordinates x1,y1,x2,y2.

        For a complete documentation, read the official
        tkinter documentation on the create_rectangle method:
        https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html#Canvas.create_rectangle
        """
        self._verify_enabled()
        idnum: int = super().create_rectangle(*args, **kwargs)
        self._calls.append((idnum, "create_rectangle", args, kwargs))
        return idnum

    def create_text(self, *args: Any, **kwargs: Any) -> int:
        """
        Create text with coordinates x1,y1.
        
        For a complete documentation, read the official
        tkinter documentation on the create_text method:
        https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html#Canvas.create_text
        """
        self._verify_enabled()
        idnum: int = super().create_text(*args, **kwargs)
        self._calls.append((idnum, "create_text", args, kwargs))
        return idnum


def _pil_to_photoimage(call_kwargs: dict[str, Any]):
    if 'image' in call_kwargs and 'pil_image' in call_kwargs:
        raise Exception('create_image: uib_inf100_graphics.simple does'
            + ' not support both image= and pil_image= parameters'
            + ' at the same time.')
    if 'image' in call_kwargs:
        if isinstance(call_kwargs['image'], Image.Image):
            raise Exception("create_image: 'image' parameter can not be an"
                    + " instance of a PIL/Pillow image. Use the 'pil_image'"
                    + 'parameter instead.')
    elif 'pil_image' in call_kwargs:
        pil_image = call_kwargs['pil_image']
        del call_kwargs['pil_image']
        if isinstance(pil_image, Image.Image):
            call_kwargs['image'] = ImageTk.PhotoImage(pil_image)
        else:
            raise Exception('create_image: pil_image value is not an instance'
                + ' of a PIL/Pillow image. Use the load_image function from'
                + ' uib_inf100_graphics.imagetools package to load image as'
                + ' a PIL/Pillow image.')
    else:
        raise Exception("create_image: canvas from uib_inf100_graphics.simple"
                + " should use the 'pil_image' parameter")
