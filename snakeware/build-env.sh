#!/bin/sh

# requires wget, ar, tar, mount, umount, dirname and readlink.
# also any debootstrap dependencies: https://packages.ubuntu.com/focal/debootstrap
# tested on busybox versions of all of these

set -eu

ROOT_COMMAND="sudo" # will prefix any commands requiring root privileges with this

CODENAME="focal" # version of Ubuntu (or Debian)
MIRROR="http://archive.ubuntu.com/ubuntu/"
DEBOOTSTRAP="$MIRROR/pool/main/d/debootstrap/debootstrap_1.0.118ubuntu1.1_all.deb"

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

WORKDIR="$SCRIPT_DIR/work"
BUILDDIR="$WORKDIR/build" 
SNAKEWARE_ROOT="$SCRIPT_DIR/../"

mkdir -p "$WORKDIR"

if [ ! -d "$BUILDDIR" ]; then
	debfile="$WORKDIR/bootstrap.deb"

	if [ ! -f "$debfile" ]; then
		wget "$DEBOOTSTRAP" -O "$debfile"
	fi

	# it's like pushd but more compatible
	CURR="$PWD" 
	cd "$WORKDIR"
	
	ar x "$debfile"
	tar xf "data.tar.gz"

	# tidy up
	rm data.tar.gz control.tar.gz debian-binary

	# go back up
	cd "$CURR"

	"$ROOT_COMMAND" env DEBOOTSTRAP_DIR="$WORKDIR/usr/share/debootstrap/" \
		"$WORKDIR/usr/sbin/debootstrap" \
		--variant buildd --arch amd64 \
		--include "bc,ca-certificates,cpio,fakeroot,file,git,kpartx,libelf-dev,libglib2.0-0,libpython3.8,libssl-dev,libncurses-dev,mercurial,python3.8,rsync,sudo,unzip,wget" \
		"$CODENAME" "$BUILDDIR" "$MIRROR"

	"$ROOT_COMMAND" cp "$SCRIPT_DIR/build-env-init.sh" "$BUILDDIR/init"
fi

# id -u and id -g are used so the user has easy access to the
# build files as their regular user outside the chroot

"$ROOT_COMMAND" mkdir -p "$BUILDDIR/snakeware"
"$ROOT_COMMAND" chown "$(id -u)":"$(id -g)" -R "$BUILDDIR/snakeware"

exec "$ROOT_COMMAND" env SNAKEWARE_ROOT="$SNAKEWARE_ROOT" \
	"$SCRIPT_DIR/build-env-chroot.sh" "$BUILDDIR" /init \
	"$(id -u)" "$(id -g)"
