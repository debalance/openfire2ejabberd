# openfire2ejabberd
a bunch of scripts to migrate an openfire database to ejabberd

## A few notes

This bunch of scripts was used to migrate the XMPP server of the RWTH Aachen University from openfire 3.9.3 to ejabberd 16.09,
but probably works with newer versions of openfire and ejabberd as well.
The conversion scripts were used with python 3.5.1.

The file openfire_cipher.py was provided publicly on
https://community.igniterealtime.org/thread/50526
and its copy in this repository is merely a backup of that.
It has "Copyright 2013, Julien Lefeuvre" and is licensed under "CeCILL-B - http://www.cecill.info/licences.en.html",
a French Free Software license, compatible with the GNU GPL.

The rest was written by me,
Philipp Huebner (debalance @ debian.org),
in 2016 and is licensed under GPL 3+.

The import to ejabberd via shell script is definitely not the fastest possibility,
but it is quite sturdy and easy to adjust.

Likewise, I don't claim to be an amazing software developer,
so my scripts here are not as efficient as they could be,
but they worked 100% reliably.
Take 'em or leave 'em.

The database migration is not a complete one,
you'll definitely loose some information,
but the more important stuff is covered.

The key to decrypt the passwords is stored in the database:
> select propvalue from ofProperty where name = 'passwordKey';

You need to put it in convert1_user.py

## General usage
1. Get your passwordKey (see above) and put it in convert1_user.py
2. In every file, replace jabber.rwth-aachen.de with your XMPP domain.
3. Put your mysql password for the openfire database into mysql.cnf.
4. Copy mysql.cnf and export-openfire.sh to the machine running openfire.
5. On the machine running openfire, execute export-openfire.sh
6. Sync the resulting files in the folder "from-openfire" to your machine
7. Execute conversion scripts
8. Sync the resulting files in the folter "to-ejabberd" to your machine running ejabberd
9. Execute import scripts
