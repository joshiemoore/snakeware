# cpumon
Displays a bar graph of CPU usage.

The graph goes from 0% at the bottom to 100% at the top, showing combined CPU use of all cores/threads. It's 100 px high, so each pixel vertically equals one percent. This is for all threads combined, so e.g. if on my Ryzen with its 16 threads there are 8 threads running at 100% and the other 8 are idle, the graph would show 50% total CPU use.

Horizontally, the graph is 200px wide, so being set to 4 FPS, it shows the last 50 s.

Data is either read via ``psutil`` if available or directly from ``/proc/stat`` (only works on Linux).

# Author

Martin C. Doege

+ github: https://github.com/mdoege

+ date: 5 Jun 2020
