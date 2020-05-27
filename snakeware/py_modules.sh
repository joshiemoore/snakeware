# Install python modules
# Run this after the build.sh script finishes.

build/usr/bin/python3 -m pip install -r config/pip_modules.txt

# snakeware python packages
cp ../snakewm/snakewm.py build/usr/lib/python3.8/
