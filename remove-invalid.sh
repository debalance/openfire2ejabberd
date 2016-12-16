#!/bin/sh

for USER in `./user_dicts.py`; do
	for FILE in ./to-ejabberd/*.sh; do
		sed -i "/$USER/d" "$FILE"
	done
	sed -i "/$USER/d" "from-openfire/users.out"
done
