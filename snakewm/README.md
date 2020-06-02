# Snake Window Manager
snakewm is a basic window manager built using the pygame and pygame-gui packages.

## Running snakewm
To launch snakewm in snakeware, use commands:

```
>>> from snakewm.wm import SnakeWM
>>> SnakeWM().run()
```

snakewm can also be run independently of snakeware on other operating systems with python3 installed.  This can be
used to develop and test new snakeware compatible apps without building a new distro image for every change.

To run snakewm on macOS and Linux distributions:

```/.../snakewm$ sudo python wm.py```

To run snakewm on Windows:

```PS C:\...\snakewm> python wm.py```


To escape snakewm press `ALT-ESC`, or go to `system>exit snakewm` from the apps menu.

To run snakewm properly on other OSs you will need to have several PIP packages installed.  It is recommended this is 
done within a [python virtual environment](https://docs.python.org/3/library/venv.html), to avoid package dependency 
clashes with other projects.

To install PIP packages type command `python -m pip install <package name>`

**Required PIP Packages**
+ For window manager
    + [pygame](https://pypi.org/project/pygame/)
    + [pygame-gui](https://pypi.org/project/pygame-gui/)
+ For speaknspell
    + [pyttsx3](https://pypi.org/project/pyttsx3/)
	+ [pywin32](https://pypi.org/project/pywin32/) (if on Windows)
	+ [comtypes](https://pypi.org/project/comtypes/) (if on Windows)
+ (list will likely increase as more apps use PIP packages)
