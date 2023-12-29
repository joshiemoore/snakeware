# rammon

Displays a bar graph of RAM usage.

The graph goes from 0% at the bottom to 100% at the top, showing combined RAM use of all cores/threads.
It's 100 px high, so each pixel vertically equals one percent.

Horizontally, the graph is 200px wide, so being set to 4 FPS, it shows the last 50 s.

Data is read directly ``/proc/meminfo`` (only works on Linux), using ``MemTotal`` and ``MemAvailable`` entries.
This is forked from cpumon, and shares the majority of its code with it.

# Author

Based heavily on cpumon Martin C. Doege

+ github: https://github.com/mdoege

+ date: 5 Jun 2020

Change from CPU usage to RAM made by pavo

+ github: https://github.com/callmepavo

+ date: 9 July 2020
