# generate the initrd.img file
SNAKEWARE=$PWD
BLD=$SNAKEWARE/build

cd $BLD
rm -f $BLD/boot/initrd.img
find .  -print | cpio -o -H newc | gzip -9 > $BLD/boot/initrd.img
