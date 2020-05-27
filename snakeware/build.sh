# This script downloads and builds linux and python sources, and outputs
# the snakeware structure in the build/ directory.

# linux kernel version
KERNEL_MAJ=v5.x
KERNEL_MIN=5.6.14

# python version
PYTHON_VER=3.8.3

# snakeware dirs
SNAKEWARE=$PWD
SRC=$PWD/src
BLD=$PWD/build

mkdir -p $SRC

mkdir -p $BLD
mkdir -p $BLD/etc/init.d $BLD/proc $BLD/sys $BLD/dev $BLD/tmp $BLD/boot $BLD/bin

chmod 1777 $BLD/tmp


# copy libs
#\TODO build these libs from source
mkdir -p $BLD/usr/lib $BLD/usr/lib64

# python dependencies
cp /usr/lib/libcrypt.so.1 $BLD/usr/lib
cp /usr/lib/libc.so.6 $BLD/usr/lib/
cp /usr/lib/libpython3.8.so.1.0 $BLD/usr/lib/
cp /usr/lib64/ld-linux-x86-64.so.2 $BLD/usr/lib64/
cp /usr/lib/libpthread.so.0 $BLD/usr/lib/
cp /usr/lib/libdl.so.2 $BLD/usr/lib/
cp /usr/lib/libutil.so.1 $BLD/usr/lib/
cp /usr/lib/libm.so.6 $BLD/usr/lib/
cp /lib/libgcc_s.so.1 $BLD/usr/lib/

# pygame dependencies
cp /usr/lib/libSDL-1.2.so.0 $BLD/usr/lib/
cp /usr/lib/libz.so.1 $BLD/usr/lib/
cp /lib/libSDL_ttf-2.0.so.0 $BLD/usr/lib/
cp /lib/libfreetype.so.6 $BLD/usr/lib/
cp /lib/libbz2.so.1.0 $BLD/usr/lib/
cp /lib/libpng16.so.16 $BLD/usr/lib/
cp /lib/libharfbuzz.so.0 $BLD/usr/lib/
cp /lib/libglib-2.0.so.0 $BLD/usr/lib/
cp /lib/libgraphite2.so.3 $BLD/usr/lib/
cp /lib/libpcre.so.1 $BLD/usr/lib/

mkdir -p $BLD/lib $BLD/lib64
cp $BLD/usr/lib/* $BLD/lib/
cp $BLD/usr/lib64/* $BLD/lib64/


# GET SOURCES
cd $SRC

if [ ! -d "linux-$KERNEL_MIN" ]; then
  echo "Downloading kernel source..."
  wget https://cdn.kernel.org/pub/linux/kernel/$KERNEL_MAJ/linux-$KERNEL_MIN.tar.xz
  tar xf linux-$KERNEL_MIN.tar.xz
  rm linux-$KERNEL_MIN.tar.xz
fi

if [ ! -d "Python-$PYTHON_VER" ]; then
  echo "Downloading python source..."
  wget https://www.python.org/ftp/python/3.8.3/Python-$PYTHON_VER.tar.xz
  tar xf Python-$PYTHON_VER.tar.xz
  rm Python-$PYTHON_VER.tar.xz
fi

if [ ! -d "busybox" ]; then
  echo "Downloading busybox source..."
  git clone https://git.busybox.net/busybox
fi

# BUILD SOURCES

# build kernel with default config
#\TODO better config?
cp $SNAKEWARE/config/kernel-config $SRC/linux-$KERNEL_MIN/.config
cd $SRC/linux-$KERNEL_MIN
make -j4
make modules
make modules_install INSTALL_MOD_PATH=$BLD/
cp arch/x86/boot/bzImage $BLD/boot/vmlinuz

# build python
cd $SRC/Python-$PYTHON_VER
./configure --prefix=$BLD/usr/
make -j4
make install

# build busybox
cd $SRC/busybox
make defconfig
export LDFLAGS="--static"
make -j4
make install

#sudo chmod 4755 _install/bin/busybox
sudo chown root _install/bin/busybox
cp -a _install/* $BLD/

rm $BLD/linuxrc
cd $BLD
ln -s bin/busybox init


# create /etc/init.d/rcS
cat << EOF > $BLD/etc/init.d/rcS
#!/bin/sh
mount -a
mdev -s
/bin/hostname -F /etc/hostname
/sbin/ifconfig lo 127.0.0.1 up

while [ 1 ]
do
  clear
  /usr/bin/python3
done

EOF

chmod +x $BLD/etc/init.d/rcS

# create /etc/fstab
cat << EOF > $BLD/etc/fstab
proc /proc proc defaults 0 0
sysfs /sys sysfs defaults 0 0
devpts /dev/pts devpts defaults 0 0
tmpfs /dev/shm tmpfs defaults 0 0
EOF

# create /etc/hostname
echo 'localhost' > $BLD/etc/hostname
