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

### Errors on archlinux/manjaro(fakeroot build problems)

To build it success we can chroot into debian/ubuntu(debian lightweight).

Install debootstrap -> `sudo pacman -S debootstrap`
After install debian-chroot -> `debootstrap stable ./buildroot-debian-stable`        
After download you can see debian-stable rootfs in dir `buildroot-debian-stable`. cd to dir.  
  Mounting pseudo-filesystems
`sudo mount proc -t proc ./proc && sudo mount sys -t sysfs ./sys && sudo mount --bind /dev ./dev && sudo mount --bind /dev/pts ./dev/pts`

Chroot! -> `chroot ./ /usr/bin/env -i HOME=/root PS1="(buildroot): "TERM="$TERM" /bin/bash --login`

Setup it. 
1. Set root password: `passwd`
2. Set timezone: `ln -sf /usr/share/zoneinfo/UTC /etc/localtime`
3. For df work -> `cat >/etc/mtab <<EOF  
rootfs / rootfs rw 0 0  
EOF`
4. Check for ethernet system: apt update
5. If you get DNS error, copy resolv.conf from **your system(not chroot)**: `cp /etc/resolv.conf ./etc/resolv.conf`
6. install dependieces: `apt install file gcc g++ make mercurial wget rsync unzip bc git`
7. Add user: `adduser builder`
8. Set password for user: passwd builder
9. su - builder
10. Go to instruction and do all steps.
11. Enjoy!
## Other info




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
