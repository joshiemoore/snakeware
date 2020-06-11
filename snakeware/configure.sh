#!/usr/bin/env bash
set -euo pipefail

# This script is used for configuring Buildroot & other components that
# have configuration in the ./external directory. It is not neccesary to
# run, and can safely be disregarded if you're doing a regular build.

# Get script path
snakeware="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

external="$snakeware/external"
buildroot="$snakeware/buildroot"

# https://buildroot.org/downloads/manual/manual.html#_configuration_of_other_components
buildroot() {
    platform="$1"

    pushd "$buildroot"
        make "BR2_EXTERNAL=$external" "${platform}_defconfig"

        make menuconfig
        make savedefconfig "DEFCONFIG=$external/configs/${platform}_defconfig"
    popd
}

linux() {
    platform="$1"

    pushd "$buildroot"
        make "BR2_EXTERNAL=$external" "${platform}_defconfig"

        make linux-menuconfig
        make linux-update-defconfig
    popd
}

busybox() {
    platform="$1"

    pushd "$buildroot"
        make "BR2_EXTERNAL=$external" "${platform}_defconfig"

        make busybox-menuconfig
    popd
}

platforms=( $external/configs/*_defconfig ) # List all configs in external/configs
platforms=( "${platforms[@]%_defconfig}" ) # Remove suffix
platforms=( "${platforms[@]##*/}" ) # Remove paths

if [ "$#" -lt 2 ]; then
    exec cat <<EOF
$0 <component> <platform>

Known components:
    buildroot
    linux
    busybox

Known platforms:
$(for file in "${platforms[@]}"; do echo "    $file"; done)
EOF
fi

sel_component="$1"
sel_platform="$2"

if [[ ! " ${platforms[@]} " =~ " ${sel_platform} " ]]; then
    exec echo "Unknown platform $sel_platform. Run without arguments for help."
fi

case "$sel_component" in
    "buildroot")
        buildroot "$sel_platform"
        ;;
    "linux")
        linux "$sel_platform"
        ;;
    "busybox")
        busybox "$sel_platform"
        ;;
    *)
        echo "Unknown component $sel_component. Run without arguments for help."
esac
