# snakeware build docs
The snakeware build system is based on buildroot and the process is almost entirely automated.

The build will take quite a long time the first time you do it, but it will only take a couple
minutes each subsequent time (unless you do a `make clean` in the buildroot directory).

Currently supported platforms:
* x86-64
* rpi4

## Build Process

### 1. Run `./build.sh <platform>`
`<platform>` should be one of the supported platforms from the above list.

This script is the longest part of the process, as it makes a clone of buildroot, which then downloads
and makes all the necessary sources.

### 2. Done!
If the build is successful, a `snakeware.iso` file will be generated and placed in this directory.

You can run this image in QEMU, or dd it to a flash drive to try running it on real hardware.

## Other info
TODO

## Ports
snakeware will always be primarily focused on x86-64, but buildroot makes it possible to build for
other platforms.

You can try porting snakeware to other platforms by creating a kernel config and a buildroot config that
both match the platform you're targeting. For example, if you were making an ARM port, you will add
the files `config/arm-buildroot-config` and `config/arm-kernel-config` and then run `./build.sh arm`.

It may be very difficult to create configs that work for the platform you're targeting, and this is not
a task for inexperienced Linux users. I do not guarantee that cross-building will work because I haven't
tried it, and you shouldn't try it unless you're pretty knowledgeable about the Linux kernel and about
buildroot.

I would be interested to hear your results if you try this, and please send a PR if you get some working configs.
