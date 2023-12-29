# cpumon

Displays a bar graph of CPU usage.

The graph goes from 0% at the bottom to 100% at the top, showing combined CPU use of all cores/threads.
It's 100 px high, so each pixel vertically equals one percent. This is for all threads combined,
so e.g. if on a system with 16 threads there are 8 threads running at 100% and the other 8 are idle,
the graph would show 50% total CPU use.

Horizontally, the graph is 200px wide, so being set to 4 FPS, it shows the last 50 s.

Data is either read via ``psutil`` if available or directly from ``/proc/stat`` (only works on Linux).

# Author

Martin C. Doege

+ github: https://github.com/mdoege

+ date: 5 Jun 2020

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

# Sysmon (System Monitor)

Displays two bars of cpu and ram usage, and displays the usages in numbers too

To see the details, scroll up to cpumon and rammon

# Author

Combined from cpumon by Martin C. Doege, and rammon by pavo.

Combined by mochidaz

+ github: https://github.com/mochidaz

+ date 27 July 2020
