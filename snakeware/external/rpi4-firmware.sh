# override rpi4 firmware configs with custom configs

SNAKEWARE=$PWD/..

# copy firmware config
cp -r $SNAKEWARE/external/rpi4-firmware/* $SNAKEWARE/buildroot_rpi4/output/images/rpi-firmware/
