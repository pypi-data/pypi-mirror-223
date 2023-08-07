# UiB INF100 Graphics

- [About](#about)
- [Installation](#installation)

For sample usage, see the docs on the [simple](./docs/simple.md), [event_app](./docs/event_app.md) and [helpers](./docs/helpers.md) subpackages, as well as the provided [examples](./examples/).

## About

UiB INF100 Graphics is a framework creating graphics and interactive applications for new beginners in programming. It consists of two subpackages: 
 - `basic`, which is intended for the first few weeks of an introductory course. This package let us create images and animations in a desktop frame with a simple, iterative programming paradigm.
 - `event_app`, which is intended for creating a first interactive, graphical desktop application.

Note that the `simple` subpackage and the `event_app` subpackage are *not* designed be used simultaneously.

> For teachers: this framework is a wrapper around a [Canvas](https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html) object from Python's [tkinter](https://docs.python.org/3/library/tkinter.html), designed to simplify the framework with these principles in mind:
> - creative learning: allow users to be creative with programming as early as possible.
> - authenticity: functions are named and behave (as far as possible) the same as for a true tkinter canvas. This gives an authentic experience and seamless transition to the more advanced framework later.
> - classes come later: knowing the object-oriented programming paradigm is not neccessary in order to use the framework.
> - the `basic` package is made for a purely iterative experience; similar to the turtle package.
> - the `event_app` package is for creating interactive applications using an event-based paradigm. It designed to enforce the use of model-view-controller.


## Installation

**Prerequisites**

Python 3.10 or above, in an installation *that includes Tkinter*. Note that the standard installer downloaded from [python.org](https://www.python.org) includes this by default, whereas some installers that are provided by package managers such as homebrew and apt-get does not, and Tkinter then needs to be installed separately.

For Linux users only, the package [pyscreenshot](https://github.com/ponty/pyscreenshot) must be installed for all features to work.

**Installation with pip through the Terminal**

1. Ensure your Python version is version 3.10 or higher. The command
```
python --version
```
should print "Python 3.10.4" or something similar. As long as it is 3.10 or higher, you're ok. If it does not immediately work, you may also try to replace "python" with `python3` or simply `py` (if so, you must make the same replacement for the commands below).

2. Ensure you are using an updated version of pip. Run
```
python -m pip install --upgrade pip
```

3. Install uib-inf100-graphics
```
python -m pip install uib-inf100-graphics
```

**Alternative installation by running a Python script**

Copy and paste the following code into a python file, and then run it.

```python
import sys
from subprocess import run

package_name = "uib-inf100-graphics"

if ((sys.version_info[0] != 3) or (sys.version_info[1] < 10)):
    raise Exception(f"{package_name} requires Python 3.10 or later. "
            + "Your current version is: "
            + f"{sys.version_info[0]}.{sys.version_info[1]}")

ans = input(f"\n\nType 'yes' to install {package_name}: ")
if ((ans.lower() == "yes") or (ans.lower() == "y")):
    print()
    cmd_pip_update = f"{sys.executable} -m pip install --upgrade pip"
    print(f"Attempting to update pip with command: {cmd_pip_update}")
    run(cmd_pip_update.split())
    
    print()
    cmd_install = f"{sys.executable} -m pip install {package_name}"
    print(f"Attempting to install {package_name} with command: {cmd_install}")
    run(cmd_install.split())
else:
    print(f"Did not attempt to install {package_name} now")
print("\n")
```
