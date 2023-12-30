"""
Read RAM usage in percent from /proc/meminfo
(only works on Linux)
"""

from string import digits
import time


def isolate_num(text):
    """Isolate num"""

    isolated_digits = ""
    for c in text:
        if c in digits:
            isolated_digits += c
    return int(isolated_digits)


def ramproc():
    """RAM proc"""

    with open("/proc/meminfo", encoding='UTF-8') as file:
        file_items = file.read().split("\n")
        total = isolate_num(file_items[0])
        used = total - isolate_num(file_items[2])  # uses memavaiable line

    perc = round((used / total) * 100)

    return perc


# Test the module
if __name__ == "__main__":
    while True:
        print(ramproc())
        time.sleep(1)
