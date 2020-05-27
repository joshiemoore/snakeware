# Install python modules
# Run this after the build.sh script finishes.

# install pip modules
build/usr/bin/python3 -m pip install -r config/pip_modules.txt

# snakeware python packages
cp -r ../snakewm/ build/usr/lib/python3.8/
