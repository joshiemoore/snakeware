# This script builds a snakeware image using buildroot.
# The first and only argument should be the platform (ie x86-64)

if [ $# != 1 ]; then
  echo "Invalid number of parameters."
  echo "Usage: ./build.sh <platform>"
  exit
fi

IMG_SIZE=400M
BUILDROOT_VERSION=2020.05

SNAKEWARE=$PWD
IMG=snakeware.img

if [ ! -d buildroot ]; then
  git clone -b $BUILDROOT_VERSION https://github.com/buildroot/buildroot.git buildroot --depth 1
fi

if [ ! -f "$SNAKEWARE/external/configs/$1_defconfig" ]; then
  echo "Unsupported platform: $1"
  exit
fi

# run build
cd buildroot
make BR2_EXTERNAL="$SNAKEWARE/external" "$1_defconfig"
make

cd $SNAKEWARE

if [ ! -f buildroot/output/images/rootfs.tar ]; then
  echo "Failed to generate rootfs.tar, not creating bootable image."
  exit
fi

# create blank image
rm -f $IMG
dd if=/dev/zero of=$IMG bs=$IMG_SIZE count=0 seek=1

#  create primary DOS partition, make it bootable, write
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
