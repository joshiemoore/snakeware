# Snake Window Manager

snakewm is a basic window manager built using the pygame and pygame-gui packages.

**Keyboard-mappings:**

+ Open/close App Menu: `SUPER`
+ Exit snakewm: `ALT+ESC`
+ Toggle dynamic backgrounds: `ALT+D`
+ snakepaint mappings
    + Toggle paint mode `ALT+P`
    + Change brush size `SCROLL`
    + Change colour `ALT+SCROLL`
    + Change brush shape `CTRL+SCROLL`

## Running snakewm on snakeware

To launch snakewm in snakeware Python shell, there are 2 ways:

1. Run the custom snakeware shell command (release 0.0.3+)

```
>>> snakewm
```

2. Run Python import manually

```
>>> from snakewm.wm import SnakeWM
>>> SnakeWM().run()
```

## Running snakewm on other OSs

snakewm can also be run independently of snakeware on other operating systems with python3 installed.
This can be used to develop and test new snakeware compatible apps without building a new distro image for every change.

To run snakewm on macOS and Linux distributions:

```/.../snakewm$ sudo python3 wm.py```

To run snakewm on Windows:

```PS C:\...\snakewm> python3 wm.py```

To escape snakewm press `ALT-ESC`, or go to `system>exit snakewm` from the App Menu.

**Note for running snakewm on macOS:**
macOS comes with Python2.7 preinstalled, not Python3. snakewm is required to be run on Python3. Latest version of
Python3 can be downloaded [here.](https://www.python.org/downloads/mac-osx/)

**Note for running snakewm on Windows:**
The App Menu in snakewm is mapped to the `SUPER Key (Start/Win key)`. When running snakewm over Windows, to open the
App Menu without triggering the Start Menu press `ALT+SUPER`.

## Dependencies

To run snakewm properly on other OSs you will need to have several PIP packages installed.
It is recommended this is done within a [Python virtual environment](https://docs.python.org/3/library/venv.html),
to avoid package dependency clashes with other projects.

To install PIP packages type command `python3 -m pip install <package name>`

**Required PIP Packages**

+ For window manager
    + [pygame](https://pypi.org/project/pygame/)
    + [pygame-gui](https://pypi.org/project/pygame-gui/)
+ For speaknspell
    + [pyttsx3](https://pypi.org/project/pyttsx3/)
    + [pywin32](https://pypi.org/project/pywin32/) (if on Windows)
    + [comtypes](https://pypi.org/project/comtypes/) (if on Windows)
+ (list will likely increase as more apps use PIP packages)
