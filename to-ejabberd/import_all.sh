#!/bin/sh

if [ "$(id -u)" != "0" ]; then
	echo "This script must be run with sudo!" 1>&2
	exit 1
fi

for SCRIPT in 1_user 2_roster 3_group 4_muc 5_vcard 6_private 7_privacy; do
	date
	echo import$SCRIPT.sh
	./import$SCRIPT.sh
done
date
