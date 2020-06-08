#!/bin/sh
# This script builds a snakeware image using buildroot.
# The first and only argument should be the platform (ie x86-64)

cleanup()
{
  set +e
  umount "$MNT" 2>/dev/null
  rm -f "$RIMG"
}

trap 'cleanup' INT TERM 0

if [ $# != 1 ]; then
  echo "Invalid number of parameters."
  echo "Usage: ./build.sh <platform>"
  exit
fi

set -e

# The final image size will be (`IMG_SIZE` + `BLOCK_SIZE` x `MBR_BLOCK_CNT`)
IMG_SIZE=400M
BUILDROOT_VERSION=2020.05

SNAKEWARE=$PWD
IMG=snakeware.img

RIMG=$IMG.rootpartition
MNT=$SNAKEWARE/mnt

# Disk/MBR parameter defaults: 2048 sectors x 512B
BLOCK_SIZE=512
MBR_BLOCK_CNT=2048

if [ ! -d buildroot ]; then
  git clone -b $BUILDROOT_VERSION https://github.com/buildroot/buildroot.git buildroot --depth 1
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

# run build
make -C buildroot

cd $SNAKEWARE

if [ ! -f buildroot/output/images/rootfs.tar ]; then
  echo "Failed to generate rootfs.tar, not creating bootable image."
  exit
fi

# create blank images for the whole disk and the root partition
rm -f "$IMG" "$RIMG"
mkdir -p "$MNT"
dd if=/dev/zero of="$IMG" bs="$BLOCK_SIZE" count="$MBR_BLOCK_CNT" conv=sparse

# NOTE: `fuse-ext2` does not support mounting a partition from a disk file offset,
# so we create a temporary partition image separately.
# Since `grub-install` requires a valid partition table to be present when running,
# we also preallocate the full size of the final disk image instead of just appending
# the root partition image at the end of the build.
# This will use twice the disk space during the build process.
truncate -s "+$IMG_SIZE" "$IMG"
truncate -s "$IMG_SIZE" "$RIMG"

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

mkfs.ext4 "$RIMG"
fuse-ext2 "$RIMG" "$MNT" -o force

# extract generated image to root partition, install grub
tar -xf $SNAKEWARE/buildroot/output/images/rootfs.tar -C $MNT
cp $SNAKEWARE/buildroot/output/images/rootfs.cpio $MNT/boot/initrd.img
mkdir -p $MNT/boot/grub
grub-install --skip-fs-probe --modules=part_msdos --root-directory="$MNT" "$IMG"
cp $SNAKEWARE/config/grub.cfg $MNT/boot/grub/grub.cfg

# copy the root partition image into the final disk image
umount "$MNT"
dd if="$RIMG" of="$IMG" bs="$BLOCK_SIZE" seek="$MBR_BLOCK_CNT" conv=sparse

chmod a+rwX "$SNAKEWARE/$IMG"
echo "Succesfully created $IMG."
