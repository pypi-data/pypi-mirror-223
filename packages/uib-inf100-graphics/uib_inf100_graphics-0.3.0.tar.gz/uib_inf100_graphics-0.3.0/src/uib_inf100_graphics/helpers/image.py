import os
from io import BytesIO
from tkinter import filedialog, Canvas
from typing import Literal

from PIL import Image
import requests

from uib_inf100_graphics.helpers.logger import _warning


def load_image_http(url: str) -> Image.Image:
    """
    Load an image from the internet.

    Parameters
    ----------
    url : str
        The URL to the image file.

    Returns
    -------
    Image.Image
        The loaded image.

    Raises
    ------
    requests.exceptions.RequestException
        If the image cannot be loaded.
    """
    return Image.open(BytesIO(requests.get(url).content))

def load_image(path: str|None=None) -> Image.Image | None:
    """
    Load an image from a file or URL. If no path is given, a file
    dialog is shown to select a file. If the path starts with 'http',
    the image is loaded from the internet. Otherwise, the image is
    loaded from a file on disk. If the user cancels the file dialog,
    None is returned. Otherwise, the loaded image is returned.
    If the image cannot be loaded, an error is raised.

    Parameters
    ----------
    path : str, optional
        The path to the image file, by default None
    
    Returns
    -------
    Image.Image or None
        The loaded image, or None if the user cancelled the file
        dialog.
    
    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    requests.exceptions.RequestException
        If the image from the internet cannot be loaded.
    """
    if (path is None):
        path = filedialog.askopenfilename(
                initialdir=os.getcwd(), 
                title='Select file: ',
                filetypes = (('Image files','*.png *.gif *.jpg'),('all files','*.*'))
        )
        if (not path): return None

    if path.startswith('http'):
        return load_image_http(path)
    return Image.open(path)

def scaled_image(image: Image.Image, scale: float, antialias: bool=False):
    """
    Scale an image by a given factor.

    Parameters
    ----------
    image : Image.Image
        The image to scale.
    scale : float
        The scale factor.
    antialias : bool, optional
        Whether to use antialiasing, by default False. Antialiasing
        produces a higher-quality image but is slower.
    
    Returns
    -------
    Image.Image
        The scaled image.
    """
    # antialiasing is higher-quality but slower
    resample = Image.ANTIALIAS if antialias else Image.NEAREST
    return image.resize(
        (round(image.width*scale), round(image.height*scale)),
        resample=resample
    )

def cropped_center(image: Image.Image, width: float, height: float) -> Image.Image:
    """
    Crop an image to a given size, keeping the center of the image.
    If the width is larger than the image width, the image is not
    cropped in the horizontal direction. If the height is larger than
    the image height, the image is not cropped in the vertical
    direction.

    Parameters
    ----------
    image : Image.Image
        The image to crop.
    width : float
        The width of the cropped image.
    height : float
        The height of the cropped image.

    Returns
    -------
    Image.Image
        The cropped image.
    """
    # crop to center
    x1 = max(0, (image.width - width) / 2)
    y1 = max(0, (image.height - height) / 2)
    x2 = min(x1 + width, image.width)
    y2 = min(y1 + height, image.height)
    return image.crop((x1, y1, x2, y2)) # type: ignore

def image_in_box(canvas: Canvas,
                  x1: float, y1: float, x2: float, y2: float,
                  pil_image: Image.Image,
                  fit_mode: Literal['contain', 'fill', 'crop', 'stretch']='contain',
                  antialias: bool=False):
    """
    Create an image on a canvas, fitting it into a given rectangle.
    The image is scaled and/or cropped to fit the rectangle. The
    rectangle is specified by the coordinates of its top-left and
    bottom-right corners. The image is centered within the rectangle.

    Parameters
    ----------
    canvas : Canvas
        The canvas on which to create the image.
    x1 : float
        The x-coordinate of the top-left corner of the rectangle.
    y1 : float
        The y-coordinate of the top-left corner of the rectangle.
    x2 : float
        The x-coordinate of the bottom-right corner of the rectangle.
    y2 : float
        The y-coordinate of the bottom-right corner of the rectangle.
    pil_image : Image.Image
        The image to create.
    fit_mode : Literal['contain', 'fill', 'crop', 'stretch'], optional
        The fit mode, by default 'contain'. The fit mode determines
        how the image is scaled to fit the rectangle. The following
        fit modes are available:
        - 'contain': The image is scaled to fit inside the rectangle
            while preserving the aspect ratio. The entire image is
            visible, but the rectangle may not be completely filled.
        - 'fill': The image is scaled to fill the entire rectangle
            while preserving the aspect ratio. The entire rectangle
            is filled, but the image may not be completely visible.
        - 'crop': The image is not scaled, but cropped to fit the
            rectangle if necessary. There is no guarantee that the
            entire image is visible or that the entire rectangle is
            filled.
        - 'stretch': The image is scaled to fill the entire rectangle
            without preserving the aspect ratio. The entire rectangle
            is filled and the intire image is visible, but the image
            may be distorted.
    antialias : bool, optional
        Whether to use antialiasing, by default False. Antialiasing
        produces a higher-quality image but is slower.
    """
    x1, x2, cx = min(x1, x2), max(x1, x2), (x1 + x2)/2
    y1, y2, cy = min(y1, y2), max(y1, y2), (y1 + y2)/2

    if x1 == x2 or y1 == y2:
        _warning('create_within: rectangle has zero width or height,'
                 + ' no image created')
        return

    target_width = x2-x1
    target_height = y2-y1

    scale_x = target_width / pil_image.width
    scale_y = target_height / pil_image.height

    if fit_mode == 'contain':
        scale = min(scale_x, scale_y)
        pil_image = scaled_image(pil_image, scale, antialias=antialias)
    elif fit_mode == 'fill':
        scale = max(scale_x, scale_y)
        pil_image = scaled_image(pil_image, scale, antialias=antialias)
    elif fit_mode == 'stretch':
        resample = Image.ANTIALIAS if antialias else Image.NEAREST
        pil_image = pil_image.resize((round(target_width), round(target_height)),
                             resample=resample)
    pil_image = cropped_center(pil_image, target_width, target_height)
    return canvas.create_image(
        cx, cy,
        pil_image=pil_image
    )
