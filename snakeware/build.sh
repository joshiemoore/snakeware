# This script builds a snakeware image using buildroot.
# The first and only argument should be the platform (ie x86-64)

if [ $# != 1 ]; then
  echo "Invalid number of parameters."
  echo "Usage: ./build.sh <platform>"
  exit
fi

IMG_SIZE=400M

SNAKEWARE=$PWD
IMG=snakeware.img

# check for existence of .git to make sure empty directories can still
# be cloned to
if [ ! -d "buildroot/.git" ]; then
  git clone https://github.com/buildroot/buildroot.git buildroot --depth 1
fi

if [ ! -f $SNAKEWARE/config/$1-buildroot-config ]; then
  echo "Unsupported platform: $1"
  exit
fi

# copy buildroot config and kernel config
cp $SNAKEWARE/config/$1-buildroot-config $SNAKEWARE/buildroot/.config
cp $SNAKEWARE/config/$1-kernel-config $SNAKEWARE/buildroot/configs/snakeware-kernel

# copy rootfs overlay
rm -rf $SNAKEWARE/buildroot/overlay
cp -r $SNAKEWARE/overlay $SNAKEWARE/buildroot/

# copy custom packages
# todo: edit Config.in instead of completely replacing it
cp -r $SNAKEWARE/package/* $SNAKEWARE/buildroot/package

# run build
cd buildroot
make

cd $SNAKEWARE

if [ ! -f buildroot/output/images/rootfs.tar ]; then
  echo "Failed to generate rootfs.tar, not creating bootable image."
  exit
fi

# create blank image
rm -f $IMG
dd if=/dev/zero of=$IMG bs=$IMG_SIZE count=0 seek=1

# create primary DOS partition, make it bootable, write
(
    echo o
    echo n
    echo p
    echo
    echo
    echo
    echo a
    echo w
) | fdisk $SNAKEWARE/$IMG

# create virtual block device
sudo kpartx -a $SNAKEWARE/$IMG

echo ""
echo "A virtual block device has been created for $IMG."
echo "Use lsblk to find the number of this device and run ./img_final.sh <num>"
echo "Example: ./img_final.sh 0 for loop0"
