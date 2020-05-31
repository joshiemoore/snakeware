#!/bin/sh -eu

bUID="$1"
bGID="$2"

# create user for build purposes
if ! id "snakeware" >/dev/null 2>&1; then
	addgroup snakeware \
		--gid "$bGID" \
		--quiet

	adduser snakeware \
		--home /snakeware \
		--shell /bin/bash \
		--no-create-home \
		--gecos "Snakeware Build User" \
		--uid "$bUID" \
		--gid "$bGID" \
		--disabled-password \
		--quiet
fi

if [ ! -f "/etc/profile.d/99-snakeware.sh" ]; then
	cat > /etc/profile.d/99-snakeware.sh <<'EOF'
echo ""
echo "You are now in the snakeware build environment"
echo "Run 'exit' to exit"
echo "This is just a lighter version of Ubuntu, so feel free to mess around"
echo ""
echo "If you want to reset everything, exit and remove the work directory"
echo "(You'll need root access for it)"
echo ""

export PS1="\[\033[38;5;8m\]\w\[$(tput sgr0)\] \\$\[$(tput sgr0)\] "
cd /snakeware/snakeware
EOF
fi

# enable passwordless sudo for the build user
if [ ! -f "/etc/sudoers.d/snakeware" ]; then
	echo "snakeware ALL=(ALL:ALL) NOPASSWD: ALL" > /etc/sudoers.d/snakeware
	chmod 440 /etc/sudoers.d/snakeware
fi

# add extra repositories
if [ -z "$(grep "^deb-src" "/etc/apt/sources.list")" ]; then 
	cat >> /etc/apt/sources.list <<'EOF'
deb http://archive.ubuntu.com/ubuntu focal universe
deb-src http://archive.ubuntu.com/ubuntu focal main
deb-src http://archive.ubuntu.com/ubuntu focal universe
EOF

	apt-get update -y
	apt-get build-dep python3-pygame -y
fi

# start a login shell, let the user do what they want to do
exec su snakeware -l
