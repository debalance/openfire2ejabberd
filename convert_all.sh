#!/bin/sh
for SCRIPT in 1_user 2_roster 3_group 4_muc 5_vcard 6_private 7_privacy; do
	date
	echo convert$SCRIPT.py
	./convert$SCRIPT.py
done
date
./remove-invalid.sh
date
