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

if [ ! -f buildroot/output/images/rootfs.iso9660 ]; then
  echo "Failed to generate rootfs.tar, not creating bootable image."
  exit
fi

cp buildroot/output/images/rootfs.iso9660 snakeware.iso
echo "snakeware.iso SUCCESS :)"
