#!/bin/sh -e

# Based on the kiss-chroot script
# https://github.com/kisslinux/kiss/blob/master/contrib/kiss-chroot

log() {
    printf 'I: %s.\n' "$*"
}

die() {
    log "$*" >&2
    exit 1
}

clean() {
    log Unmounting filesystems from chroot; {
        umount "$1/snakeware" ||:

        umount "$1/dev"  ||:
        umount "$1/proc" ||:
        umount "$1/sys"  ||:

        umount "$1"      ||:
    }

    log Cleaning leftover host files; {
        rm -f "$1/etc/resolv.conf"
    }
}

mounted() {
    # This is a pure shell mountpoint implementation. We're dealing
    # with basic (and fixed/known) input so this doesn't need to
    # handle more complex cases.
    [ -e "$1" ]         || return 1
    [ -e /proc/mounts ] || return 1

    while read -r _ target _; do
        [ "$target" = "$1" ] && return 0
    done < /proc/mounts

    return 1
}

[ -z "$SNAKEWARE_ROOT" ] && die "Please set the SNAKEWARE_ROOT environment variable"

[ -z "$1" ]        && die Need a path to the chroot
[ -d "$1" ]        || die Given path does not exist
[ "$(id -u)" = 0 ] || die Script needs to be run as root

trap 'clean "$1"' EXIT INT

log Mounting filesystems from host; {
    # some stuff might not work without this
    mounted "$1"      || mount --bind  "$1" "$1" 

    mounted "$1/dev"  || mount -o bind /dev "$1/dev"
    mounted "$1/proc" || mount -t proc proc "$1/proc"
    mounted "$1/sys"  || mount -t sysfs sys "$1/sys"

    mounted "$SNAKEWARE_ROOT" || mount --bind "$SNAKEWARE_ROOT" "$1/snakeware"
}

log Copying /etc/resolv.conf from host; {
    cp -f /etc/resolv.conf "$1/etc"
}

log Entering chroot; {
    chroot "$@"
}
