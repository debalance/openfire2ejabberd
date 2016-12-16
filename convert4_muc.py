#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Relevant ejabberdctl commands:
#  create_room name service host
#   - create a MUC room name@service in host
#  change_room_option name service option value
#   - change an option in a MUC room
#  set_room_affiliation name service jid affiliation
#   - change an affiliation in a MUC room
#   - possible affiliations are owner, admin, member, outcast, none


# From Openfire-openfire_3_9_1/src/java/org/jivesoftware/openfire/muc/MUCRole.java:
#
#    /**
#     * Owner of the room.
#     */
#    owner(10),
#    /**
#     * Administrator of the room.
#     */
#    admin(20),
#    /**
#     * A user who is on the "whitelist" for a members-only room or who is registered
#     * with an open room.
#     */
#    member(30),
#    /**
#     * A user who has been banned from a room.
#     */
#    outcast(40),
#    /**
#     * A user who doesn't have an affiliation. This kind of users can register with members-only
#     * rooms and may enter an open room.
#     */
#    none(50);


import re           # regular expressions for string pattern matching

def create_room(input_line):
    output_line = re.sub("\n", "", input_line)
    output_line = re.sub("'", "'\"'\"'", output_line)
    return "ejabberdctl create_room '" + output_line + "' muc.jabber.rwth-aachen.de jabber.rwth-aachen.de\n"

def configure_room(input_line):
    input_line = re.sub("\n", "", input_line)
    input_line = re.sub("'", "'\"'\"'", input_line)
    input_list = re.split("\t", input_line)
    room_name = input_list[0]
    title = [room_name, "title", input_list[1]]
    description = [room_name, "description", input_list[2]]
    allow_change_subj = [room_name, "allow_change_subj", "true" if input_list[3] == "0" else "false"]
    allow_user_invites = [room_name, "allow_user_invites", "true" if input_list[7] == "0" else "false"]
    allow_visitor_nickchange = [room_name, "allow_visitor_nickchange", "true" if input_list[11] == "0" else "false"]
    anonymous = [room_name, "anonymous", "true" if input_list[9] == "1" else "false"] 
    logging = [room_name, "logging", "true" if input_list[10] == "0" else "false"]
    return_options = (title, description, allow_change_subj, allow_user_invites, allow_visitor_nickchange, anonymous, logging)
    public = [room_name, "public", "true" if input_list[3] == "0" else "false"]
    moderated = [room_name, "moderated", "true" if input_list[5] == "0" else "false"]
    members_only = [room_name, "members_only", "true" if input_list[6] == "0" else "false"]
    return_options += (public, moderated, members_only)
    if not input_list[8] == "NULL":
        password_protected = [room_name, "password_protected", "true"]
        password = [room_name, "password", input_list[8]]
        return_options += (password_protected, password)
    return return_options

def configure_affiliations(input_line):
    input_line = re.sub("\n", "", input_line)
    input_line = re.sub("'", "'\"'\"'", input_line)
    input_list = re.split("\t", input_line)
    room = input_list[0]
    jid_list = re.split(", ", input_list[1])
    if len(input_list) < 3:
        input_list.append("30")
    if input_list[2] == "10":
        affiliation = "owner"
    elif input_list[2] == "20":
        affiliation = "admin"
    elif input_list[2] == "30":
        affiliation = "member"
    elif input_list[2] == "40":
        affiliation = "outcast"
    else:
        affiliation = "none"
    affiliations = []
    for jid in jid_list:
        new_affiliation = [room, jid, affiliation]
        affiliations.append(new_affiliation)
    return affiliations


ejc = open('to-ejabberd/import4_muc.sh', 'w')

ejc.write('#!/bin/sh -x\n')

f1 = open('from-openfire/room-names.out', 'r')
for line in f1:
    room = create_room(line)
    ejc.write(room)
f1.close()

f2 = open('from-openfire/rooms.out', 'r')
for line in f2:
    room_options = configure_room(line)
    for option_list in room_options:
        ejc.write("ejabberdctl change_room_option '%s' muc.jabber.rwth-aachen.de '%s' '%s'\n" % (option_list[0], option_list[1], option_list[2]))
f2.close()

f3 = open('from-openfire/room-members.out', 'r')
for line in f3:
    room_affiliations = configure_affiliations(line)
    for affiliation_list in room_affiliations:
        ejc.write("ejabberdctl set_room_affiliation '%s' muc.jabber.rwth-aachen.de '%s' '%s'\n" % (affiliation_list[0], affiliation_list[1], affiliation_list[2]))
f3.close()

f4 = open('from-openfire/room-affiliations.out', 'r')
for line in f4:
    room_affiliations = configure_affiliations(line)
    for affiliation_list in room_affiliations:
        ejc.write("ejabberdctl set_room_affiliation '%s' muc.jabber.rwth-aachen.de '%s' '%s'\n" % (affiliation_list[0], affiliation_list[1], affiliation_list[2]))
f4.close()

ejc.close()
