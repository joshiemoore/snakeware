# snakeware build docs
The snakeware build system is based on buildroot and the process is almost entirely automated.

The build will take quite a long time the first time you do it, but it will only take a couple
minutes each subsequent time (unless you do a `make clean` in the buildroot directory).

Currently supported platforms:
* x86-64

## Build Process

### 1. Run `./build.sh <platform>`
`<platform>` should be one of the supported platforms from the above list.

This script is the longest part of the process, as it makes a clone of buildroot, which then downloads
and makes all the necessary sources. The end of the script requires root because it uses kpartx to 
create a virtual block device for the new image.

Once the script has successfully completed, use `lsblk` to make note of the drive number of the virtual
block device the script created for the new image. For example, if the script created `loop0p1`, you will
enter `0` as the argument for the next script.

### 2. Run `sudo ./img_gen.sh <num>`
This script must be run as root.

`<num>` should be the drive number of the virtual block device from the previous step.

This script formats the root partition of the image, mounts it, and copies over all the built files generated
by buildroot. It should take a relatively short amount of time.

### 3. Done!
If both scripts are successful, a `snakeware.img` file will be generated and placed in this directory.

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

I expect that the installation of Python pip packages might not work correctly when cross-building because
that is currently happening independently of buildroot.

I would be interested to hear your results if you try this, and please send a PR if you get some working configs.
