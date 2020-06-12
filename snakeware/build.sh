# This script builds a snakeware image using buildroot.
# The first and only argument should be the platform (ie x86-64)

if [ $# != 1 ]; then
  echo "Invalid number of parameters."
  echo "Usage: ./build.sh <platform>"
  exit
fi

BUILDROOT_VERSION=2020.05

SNAKEWARE=$PWD
IMG=snakeware.img

if [ ! -d buildroot_$1 ]; then
  git clone -b $BUILDROOT_VERSION https://github.com/buildroot/buildroot.git buildroot_$1 --depth 1
fi

if [ ! -f "$SNAKEWARE/external/configs/$1_defconfig" ]; then
  echo "Unsupported platform: $1"
  exit
fi

# run build
cd buildroot_$1
make BR2_EXTERNAL="$SNAKEWARE/external" "$1_defconfig"
make

cd $SNAKEWARE

if [ $1 == x86-64 ]; then
  # look for x86-64 ISO
  if [ ! -f buildroot_$1/output/images/rootfs.iso9660 ]; then
    echo "Failed to generate rootfs.iso."
    exit
  fi

  cp buildroot_$1/output/images/rootfs.iso9660 snakeware_x86-64.iso
  echo "snakeware_x86-64.iso SUCCESS :)"
elif [ $1 == rpi4 ]; then
  # look for rpi4 SD card image
  if [ ! -f buildroot_$1/output/images/sdcard.img ]; then
    echo "Failed to generate sdcard.img."
    exit
  fi

  cp buildroot_$1/output/images/sdcard.img snakeware_rpi4.img
  echo "snakeware_rpi4.img SUCCESS :)"
fi
