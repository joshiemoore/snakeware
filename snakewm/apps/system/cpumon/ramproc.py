# Read RAM usage in percent from /proc/meminfo
# (only works on Linux)

import time


def isolate_num(text):
    digits = ""
    for c in text:
        if c in "0123456789":
            digits += c
    return int(digits)


def ramproc():
    file = open("/proc/meminfo").read().split("\n")

    total = isolate_num(file[0])
    used = total - isolate_num(file[2])  # uses memavaiable line
    perc = round((used / total) * 100)
    return perc

def ramproc2():
    file = open("/proc/meminfo").read().split("\n")

    total = isolate_num(file[0])
    used = total - isolate_num(file[2])  # uses memavaiable line
    return "Ram Usage: <br>{}/{}".format(used, total)


# Test the module
if __name__ == "__main__":
    while True:
        print(ramproc2())
        print(ramproc())
        time.sleep(1)
