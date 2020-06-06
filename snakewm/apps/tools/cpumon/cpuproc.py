# Read CPU usage in percent from /proc/stat
# (only works on Linux)

import time

o = 0
t = time.time()
numcpu = 1
for l in open("/proc/stat"):
    x = l.split()
    if l[:3] == "cpu" and len(x[0]) > 3:
        numcpu = 1 + int(x[0][3:])


def cpuproc():
    global o, t
    f = open("/proc/stat").readline().split()
    q = 0.01 * (int(f[4]) - o) / (time.time() - t)
    q = 100 * (1 - q / numcpu)
    q = max(0, min(100, q))
    t = time.time()
    o = int(f[4])
    return int(q)


# Test the module
if __name__ == "__main__":
    while True:
        print(cpuproc())
        time.sleep(1)
