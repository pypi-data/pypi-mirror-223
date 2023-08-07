import atexit
import io
import sys
import time
import tkinter as tk
from typing import Final, Any

from PIL import Image

from uib_inf100_graphics.simple.RecordingCanvas import RecordingCanvas
from uib_inf100_graphics.simple.Configuration import Configuration


class SimplifiedFrame:
    """
    SimplifiedFrame represents a window frame which displays the
    content of one or more SimplifiedCanvas objects in sequence. The
    content of the window frame is updated every time the display
    method is called.
    """

    def __init__(self, tk_root: tk.Tk):
        # Internal variables initialized on object creation
        self._config: Final = Configuration()
        self._screenshots: list[dict[str, Any]] = []
        self._is_initialized: bool = False
        self._image_is_saved: bool = False
        self._is_closed: bool = False
        self._mainloop_started: bool = False
        self._next_delay: float = 0
        self._display_call_counter: int = 0
        
        # Internal variables initialized on first call to display
        self._tkroot: Final[tk.Tk] = tk_root
        self._tkCanvas: tk.Canvas
        self._recording_canvas: RecordingCanvas

        # The variable below is never referenced, but is needed to
        # prevent the garbage collector from deleting image objects.
        self._lastCanvas: RecordingCanvas

    def config(self) -> Configuration:
        """
        Returns the configuration for this SimplifiedFrame. The
        configuration object may be mutated to change the configuration
        prior to calling the display method the first time.
        """
        return self._config
        
    def display(self, canvas: RecordingCanvas,
                duration: float|None=None,
                clear_canvas: bool=True):
        """
        Moves the content from the canvas into the window frame and
        displays the content on screen. The canvas object becomes empty
        again when the content has been moved to the window frame.
        Consecutive calls to this method will clear window frame and
        replace it with the content of the latest canvas object,
        possibly after a small delay. The call is blocking, meaning
        that the program will wait until the canvas has actually been
        displayed before returning.

        The duration parameter determines how long the the image should
        be displayed at minimum before changing the window frame
        content. This is useful if you want to animate something and
        control the animation speed. If no value is specifed for
        duration, the value specified in the configuration will be used.
        The default value is 0.1 seconds.

        If the clear_canvas parameter is set to False, the canvas will
        not be cleared after the content has been moved to the window
        frame.
        """
        self._display_call_counter += 1
        self._post_config_initialization_phase()
        self._wait_until_ready()
        self._next_delay = self._config.std_duration() if duration is None else duration

        self._tkCanvas.delete(tk.ALL)
        for call in canvas._get_calls():
            getattr(self._tkCanvas, call[1])(*call[2], **call[3])
        
        # Making a copy of the current canvas despite the variable
        # never being used is necessary in order that references to
        # any PhotoImage objects created by the tk.Canvas object are
        # not lost due to garbage collection. The reference Tkinter
        # keeps to the PhotoImage objects is for some reason not enough
        # to prevent them from being collected.
        # https://stackoverflow.com/questions/27430648/tkinter-vanishing-photoimage-issue
        self._lastCallsCopy = canvas._get_calls()
        if clear_canvas:
            canvas._clear()

        self._tkCanvas.update()
        self._tkroot.update()
        self._take_screenshot_if_required(self._next_delay)
        if self._display_call_counter >= self._config.max_frames_to_save():
            self._save_as_image()

        if not self._config.show_window() and self._image_is_saved:
            sys.exit(0)

    def _wait_until_ready(self):
        if not self._config.show_window():
            return
        target_time = time.time() + self._next_delay
        while time.time() < target_time:
            time_to_sleep = max(0, min(0.1, target_time - time.time()))
            time.sleep(time_to_sleep)
            self._tkroot.update()
            if "_is_destroyed" in self._tkroot.__dict__ and self._tkroot.__dict__["_is_destroyed"]:
                sys.exit(0)

    def _post_config_initialization_phase(self):
        if not self._is_initialized:
            self._is_initialized = True
            self._config.lock()
            self._tkroot.title(self._config.title())
            if self._config.hide_window():
                self._tkroot.withdraw()
            def close_window_clicked():
                self._save_as_image()
                self._tkroot.destroy()
                self._tkroot.__dict__["_is_destroyed"] = True
            self._tkroot.protocol("WM_DELETE_WINDOW", close_window_clicked)
            self._tkCanvas = tk.Canvas(self._tkroot,
                    width=self._config.width(),
                    height=self._config.height())
            self._tkCanvas.pack()
            self._tkroot.resizable(False, False)
            atexit.register(self._closing)

    def _take_screenshot_if_required(self, duration_sec: float):
        if self._image_is_saved:
            return
        if (self._display_call_counter < self._config.max_frames_to_save() 
                and self._config.file_to_save()):
            self._screenshots.append({
                "ps": self._tkCanvas.postscript(), # type: ignore
                "duration_ms": max(1, int(duration_sec * 1000)),
            })

    def _closing(self):
        self._save_as_image()
        if self._config.show_window() and not self._mainloop_started:
            self._mainloop_started = True
            self._tkroot.mainloop()
        
    def _save_as_image(self) -> None:
        if self._image_is_saved:
            return
        self._image_is_saved = True
        configname: str = self._config.file_to_save()
        if not configname:
            return
        if len(self._screenshots) == 0:
            return
        
        position_of_last_dot = configname.rfind(".")
        corefilename: str
        extension: str
        if position_of_last_dot == -1:
            corefilename = configname
            extension = "png"
        else:
            corefilename = configname[:position_of_last_dot]
            extension = configname[position_of_last_dot + 1:]
        if len(corefilename) == 0:
            corefilename = "screenshot"
        
        postscripts = [ screenshot["ps"] for screenshot in self._screenshots]
        durations = [ screenshot["duration_ms"] for screenshot in self._screenshots]
        images = [ Image.open(io.BytesIO(ps.encode("utf-8"))) for ps in postscripts]

        save_all: bool = extension in ["gif", "tiff", "webp", "png"]
        if save_all:
            images[0].save(
                    f"{corefilename}.{extension}",
                    save_all=save_all,
                    append_images=images[1:],
                    duration=durations,
                    loop=0)
        else:
            for i in range(len(images)):
                images[i].save(f"{corefilename}_{i+1}.{extension}")
        
