import os
import traceback
from types import MappingProxyType
from typing import Final, Any, TYPE_CHECKING

from uib_inf100_graphics.helpers.logger import _warning

if TYPE_CHECKING:
    from .SimplifiedFrame import SimplifiedFrame


class Configuration:
    """
    Configuration represents the configuration of a SimplifiedFrame object.
    Configuration can be set in three ways:
    1. By calling the config() or set_[propertyname] methods on the
        SimplifiedFrame object.
    2. By setting the corresponding environment variable. The environment
        variable must be named the same as the property, but in all caps
        and without underscores.
    3. By using the default value.

    Explanation of the available properties:

    FRAMEWIDTH
        The width of the window frame in pixels as an int. Default value is
        400. To inspect the current value, use the width() method. To change
        the value, use the set_size() method on the configuration object
        or specify the FRAMEWIDTH environment variable.

    FRAMEHEIGHT
        The height of the window frame in pixels as an int. Default value is
        400. To inspect the current value, use the height() method. To change
        the value, use the set_size() method on the configuration object
        or specify the FRAMEHEIGHT environment variable.

    FRAMETITLE
        The title of the window frame as a string. Default value is "INF100".
        To inspect the current value, use the title() method. To change the
        value, use the set_title() method on the configuration object or
        specify the FRAMETITLE environment variable.

    MAXFRAMESTOSAVE
        The maximum number of frames to save as an int. Default value is 60.
        To inspect the current value, use the max_frames_to_save() method. To
        change the value, use the set_max_frames_to_save() method on the
        configuration object or specify the MAXFRAMESTOSAVE environment
        variable.

    STDDURATION
        The standard duration in seconds as a float. Default value is 0.1.
        To inspect the current value, use the std_duration() method. To
        change the value, use the set_std_duration() method on the
        configuration object or specify the STDDURATION environment variable.

    FILETOSAVE
        The file name to save the frames to as a string. Default value is "",
        which means that no frames will be saved. To inspect the current
        value, use the file_to_save() method. To change the value, use the
        set_file_to_save() method on the configuration object or specify the
        FILETOSAVE environment variable.

    HIDEWINDOW
        Whether to hide the window or not as a bool. Default value is False.
        To inspect the current value, use the hide_window() method; or for
        the opposite value, use the show_window() method. To change the value,
        use the set_hide_window() method on the configuration object or
        specify the HIDEWINDOW environment variable.

        
    (ENVPRIORITY)
        Whether to prioritize environment variables over the other ways of
        setting the configuration as a bool. Default value is False, which
        means that any call to the config() or set_[propertyname] methods
        will take priority over the environment variables. To change the
        value, specify the ENVPRIORITY environment variable to be TRUE or 1.
        This value is not available to specify with a method on the
        configuration object.
    """

    _DEFAULT_VALUES: Final = MappingProxyType({
        "FRAMEWIDTH": 400,
        "FRAMEHEIGHT": 400,
        "FRAMETITLE": "INF100",
        "MAXFRAMESTOSAVE": 60,
        "STDDURATION": 0.1,
        "FILETOSAVE": "",
        "HIDEWINDOW": False,
    })

    def __init__(self):
        self._locked: bool = False
        self._env_priority: Final[bool] = self._get_env_priority()
        self._env_values: Final[dict[str, Any]] = {}
        self._obj_values: Final[dict[str, Any]] = {}
        self._load_from_env()

    def lock(self):
        """Locks the configuration object to prevent further changes."""
        self._locked = True

    def _get_env_priority(self) -> bool:
        value = os.environ.get("ENVPRIORITY")
        return isinstance(value, str) and value.lower() in ("true", "t", "1")

    def _load_from_env(self):
        for env_key in Configuration._DEFAULT_VALUES:
            env_value = os.environ.get(env_key)
            if env_value is not None:
                self._convert_and_insert_or_warn(self._env_values,
                                                 env_key, env_value)

    def _convert_and_insert_or_warn(self, target_dict: dict[str, Any],
                                    key: str, value: Any):
        if key not in Configuration._DEFAULT_VALUES:
            raise KeyError(f"Property {key} is not supported.")
        
        target_type = type(Configuration._DEFAULT_VALUES[key])
        try:
            if target_type == bool and type(value) == str:
                value = value.lower() in ("true", "t", "1")
            else:   
                value = target_type(value)
            target_dict[key] = value
        except ValueError as e:
            trace = traceback.extract_tb(e.__traceback__)
            trace = trace[:-1] # Remove the latest function call
            traceback_str = ''.join(traceback.format_tb(trace)) # type: ignore
            _warning(f"Property {key} must be of type"
                    + f" {target_type}, but automatic conversion failed for"
                    + f" value {repr(value)}. Assignment will be ignored. "
                    + f"Traceback:\n{traceback_str}")

    def _get_property(self, key: str) -> Any:
        """Returns the value of the property with the given key."""
        if key not in Configuration._DEFAULT_VALUES:
            raise KeyError(f"Property {key} is not supported.")
        
        if self._env_priority and key in self._env_values:
            return self._env_values[key]
        elif key in self._obj_values:
            return self._obj_values[key]
        elif key in self._env_values:
            return self._env_values[key]
        else:
            return Configuration._DEFAULT_VALUES[key]
        
    def width(self) -> int:
        """Returns the configured width of the window frame in pixels."""
        return int(self._get_property("FRAMEWIDTH"))
    
    def height(self) -> int:
        """Returns the configured height of the window frame in pixels."""
        return int(self._get_property("FRAMEHEIGHT"))
    
    def title(self) -> str:
        """Returns the configured title of the window frame."""
        return str(self._get_property("FRAMETITLE"))
    
    def max_frames_to_save(self) -> int:
        """
        Returns the maximum number of frames to save. Only matters if
        file_to_save() is not an empty string.
        """
        return int(self._get_property("MAXFRAMESTOSAVE"))
    
    def std_duration(self) -> float:
        """Returns the standard minimum duration of a frame in seconds."""
        return float(self._get_property("STDDURATION"))
    
    def file_to_save(self) -> str:
        """Returns the file name in which to save the frames."""
        return str(self._get_property("FILETOSAVE"))
    
    def hide_window(self) -> bool:
        """Returns whether the window will be hidden or not."""
        return bool(self._get_property("HIDEWINDOW"))
    
    def show_window(self) -> bool:
        """Returns whether the window will be visible or not."""
        return not self.hide_window()
    
    def set_properties(self, config_map: dict[str, Any]):
        """
        Sets the configuration properties specified in the config_map
        argument. The config_map argument must be a dictionary with string
        keys and values of the correct type. The supported properties,
        their types and default values are listed below.
        
        FRAMEWIDTH: int = 400
        FRAMEHEIGHT: int = 400
        FRAMETITLE: str = "INF100"
        MAXFRAMESTOSAVE: int = 60
        STDDURATION: float = 0.1
        FILETOSAVE: str = ""
        HIDEWINDOW: bool = False

        The ENVPRIORITY property is not supported by this method.
        """
        self._assert_configuration_is_unlocked()
        for key, value in config_map.items():
            if self._env_priority and key in self._env_values:
                _warning(f"Program runs with ENVPRIORITY=True,"
                        + f" and the property {key} was already set to"
                        + f" {repr(self._env_values[key])} by an environment"
                        + f" variable. Setting the property to"
                        + f" {repr(value)} will be ignored.")
                return
            if key in self._env_values:
                _warning(f"Property {key} was set to the value"
                        + f" {repr(self._env_values[key])} by an environment"
                        + f" variable, but this is overwritten by setting the"
                        + f" property to {repr(value)} by calling methods on"
                        + " the configuration object.")
            self._convert_and_insert_or_warn(self._obj_values, key, value)

    def _assert_configuration_is_unlocked(self):
        if self._locked:
            raise Exception("Configuration is locked, and can therefore not"
                            + " be changed. The configuration is locked when the"
                            + " 'display' function is called for the first"
                            + " time, so make sure all configuration is complete"
                            + " before making that call.")

    def set_title(self, title: str):
        """Sets the title of the window frame."""
        self.set_properties({"FRAMETITLE": title})

    def set_size(self, width: int, height: int):
        """Sets the size of the window frame in pixels."""
        self.set_properties({"FRAMEWIDTH": width, "FRAMEHEIGHT": height})

    def set_max_frames_to_save(self, max_frames_to_save: int):
        """
        Sets the maximum number of frames to save. Note that if this
        number is very large, then the saved images may take up a lot of
        space, or the program may run out of memory. This property is
        ignored if the FILETOSAVE property is not set.
        """
        self.set_properties({"MAXFRAMESTOSAVE": max_frames_to_save})

    def set_std_duration(self, std_duration: float):
        """Sets the standard duration of each frame in seconds. """
        self.set_properties({"STDDURATION": std_duration})

    def set_file_to_save(self, save_to_file: str):
        """
        Sets the file name to save the frames to. If this property is
        set to an empty string, then the frames will not be saved.
        """
        self.set_properties({"FILETOSAVE": save_to_file})

    def set_hide_window(self, hide_window: bool):
        """
        Sets whether to hide the window or not. If this property is
        set to True, then the window will not be shown, but the frames
        will still be saved if the FILETOSAVE property is set.
        """
        self.set_properties({"HIDEWINDOW": hide_window})
