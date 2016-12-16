#!/bin/sh
mkdir -p from-openfire/tables

for table in `mysql --defaults-extra-file=mysql.cnf -D wildfire --batch --skip-column-names -e "show tables;"`; do
	mysql --defaults-extra-file=mysql.cnf --database=wildfire --table << EOF > from-openfire/tables/"$table".description
DESCRIBE $table;
EOF
	mysql --defaults-extra-file=mysql.cnf --database=wildfire --skip-column-names << EOF > from-openfire/tables/"$table".out
SELECT * FROM $table;
EOF
done

# for convert1_user.py
mysql --defaults-extra-file=mysql.cnf --database=wildfire --skip-column-names << EOF > from-openfire/users.out
SET NAMES 'utf8';
SELECT username, plainPassword, encryptedPassword, name, email, creationDate FROM ofUser;
EOF

# for convert2_roster.py
mysql --defaults-extra-file=mysql.cnf --database=wildfire --skip-column-names << EOF > from-openfire/rosters.out
SET NAMES 'utf8';
SELECT ofRoster.username, ofRoster.jid, ofRoster.nick, ofRosterGroups.groupName, ofRoster.sub FROM ofRoster LEFT JOIN ofRosterGroups ON ofRoster.rosterID = ofRosterGroups.rosterID;
EOF

# for convert3_group.py
mysql --defaults-extra-file=mysql.cnf --database=wildfire --skip-column-names << EOF > from-openfire/groups.out
SET NAMES 'utf8';
SELECT ofGroup.groupName, ofGroup.description, ofGroupProp.name, ofGroupProp.propValue FROM ofGroup JOIN ofGroupProp ON ofGroup.groupName = ofGroupProp.groupName WHERE ofGroupProp.name = 'sharedRoster.groupList';
EOF
mysql --defaults-extra-file=mysql.cnf --database=wildfire --skip-column-names << EOF > from-openfire/group-members.out
SET NAMES 'utf8';
SELECT username, groupName from ofGroupUser;
EOF
mysql --defaults-extra-file=mysql.cnf --database=wildfire --skip-column-names << EOF > from-openfire/group-displays.out
SET NAMES 'utf8';
SELECT ofGroup.groupName, ofGroupProp.propValue FROM ofGroup JOIN ofGroupProp ON ofGroup.groupName = ofGroupProp.groupName WHERE ofGroupProp.name = 'sharedRoster.showInRoster';
EOF

# for convert4_muc.py
mysql --defaults-extra-file=mysql.cnf --database=wildfire --skip-column-names << EOF > from-openfire/room-names.out
SET NAMES 'utf8';
SELECT name FROM ofMucRoom;
EOF
mysql --defaults-extra-file=mysql.cnf --database=wildfire --skip-column-names << EOF > from-openfire/rooms.out
SET NAMES 'utf8';
SELECT name, naturalName, description, canChangeSubject, publicRoom, moderated, membersOnly, canInvite, roomPassword, canDiscoverJID, logEnabled, canChangeNick, canRegister FROM ofMucRoom;
EOF
mysql --defaults-extra-file=mysql.cnf --database=wildfire --skip-column-names << EOF > from-openfire/room-affiliations.out
SET NAMES 'utf8';
SELECT ofMucRoom.name, ofMucAffiliation.jid, ofMucAffiliation.affiliation FROM ofMucRoom JOIN ofMucAffiliation ON ofMucRoom.roomID = ofMucAffiliation.roomID;
EOF
mysql --defaults-extra-file=mysql.cnf --database=wildfire --skip-column-names << EOF > from-openfire/room-members.out
SET NAMES 'utf8';
SELECT ofMucRoom.name, ofMucMember.jid FROM ofMucRoom JOIN ofMucMember ON ofMucRoom.roomID = ofMucMember.roomID;
EOF

# for convert5_vcard.py
mysql --defaults-extra-file=mysql.cnf --database=wildfire --skip-column-names << EOF > from-openfire/vcards.out
SET NAMES 'utf8';
SELECT username, vcard FROM ofVCard;
EOF

# for convert6_private.py
mysql --defaults-extra-file=mysql.cnf --database=wildfire --skip-column-names << EOF > from-openfire/private.out
SET NAMES 'utf8';
SELECT username, privateData, namespace FROM ofPrivate;
EOF

# for convert7_privacy.py
mysql --defaults-extra-file=mysql.cnf --database=wildfire --skip-column-names << EOF > from-openfire/privacy.out
SET NAMES 'utf8';
SELECT username, list, isDefault FROM ofPrivacyList;
EOF

