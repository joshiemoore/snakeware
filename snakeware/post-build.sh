# This script is run by buildroot after it has finished building the rootfs, but before
# packing the final image.

# set this to the current Python 3.x version
PYLIBVER=python3.8

SNAKEWARE=$PWD/..

# install pip modules
$SNAKEWARE/buildroot/output/target/usr/bin/python3 -m pip install -r $SNAKEWARE/config/pip_modules.txt

# copy snakewm
rm -rf $SNAKEWARE/buildroot/output/target/usr/lib/$PYLIBVER/snakewm
cp -r $SNAKEWARE/../snakewm $SNAKEWARE/buildroot/output/target/usr/lib/$PYLIBVER/
