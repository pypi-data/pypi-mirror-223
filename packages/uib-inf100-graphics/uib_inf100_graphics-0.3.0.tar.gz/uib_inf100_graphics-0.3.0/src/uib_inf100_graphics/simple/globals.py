from tkinter import Tk
from typing import Final

from uib_inf100_graphics.simple.SimplifiedFrame import SimplifiedFrame
from uib_inf100_graphics.simple.RecordingCanvas import RecordingCanvas


_tk_root = Tk()
_frame: Final = SimplifiedFrame(_tk_root)
canvas: Final = RecordingCanvas(_tk_root)    
config: Final = _frame.config()

def display(canvas: RecordingCanvas, min_duration_sec: float|None=None,
            clear_canvas: bool=True):
    _frame.display(canvas, min_duration_sec, clear_canvas)