# Generate snakeware img file.
# This script must be run as root.

# snakeware image path
SNAKEWARE=$PWD
IMG=snakeware.img

# image size (MiB)
IMG_SIZE=400

MNT=/mnt

# create empty image file
dd if=/dev/zero of=$SNAKEWARE/$IMG bs=1M count=$IMG_SIZE

# create primary DOS partition, make it bootable, write
#\TODO automate this
cfdisk $SNAKEWARE/$IMG

kpartx -a $SNAKEWARE/$IMG

mkfs.ext4 /dev/mapper/loop0p1

mount /dev/mapper/loop0p1 $MNT

# copy build directory to root partition
rsync -varh $SNAKEWARE/build/ $MNT

mkdir -p $MNT/boot/grub

grub-install --root-directory=$MNT /dev/loop0
cp $SNAKEWARE/config/grub.cfg $MNT/boot/grub/grub.cfg

# unmount everything
umount $MNT
kpartx -d $SNAKEWARE/$IMG

# don't require root to access the img file
chmod a+rwX snakeware.img
