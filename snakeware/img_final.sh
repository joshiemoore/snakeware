# copy generated rootfs to the virtual block device created by build.sh
# the first argument should be the number of the loop device, so you would
# enter 1 if the device was loop1
#
# this script must be run as root

SNAKEWARE=$PWD
IMG=snakeware.img
MNT=/mnt

MAP=/dev/mapper

if [ $# != 1 ]; then
  echo "Incorrect number of parameters."
  exit
fi

mkfs.ext4 $MAP/loop$1p1

mount $MAP/loop$1p1 $MNT

# extract generated image to root partition
tar -xf $SNAKEWARE/buildroot/output/images/rootfs.tar -C $MNT

mkdir -p $MNT/boot/grub

cp $SNAKEWARE/buildroot/output/images/rootfs.cpio $MNT/boot/initrd.img

grub-install --root-directory=$MNT /dev/loop$1

# unmount everything
umount $MNT
kpartx -d $SNAKEWARE/$IMG

chmod a+rwX $SNAKEWARE/$IMG
