#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Relevant ejabberdctl commands:
#  ejabberdctl srg_create group host name description display
#   - create a Shared Roster Group
#   - If you want to specify several group identifiers in the Display argument, 
#     put \ " around the argument and separate the identifiers with \ \ n
#     For example:
#     ejabberdctl srg_create group3 localhost name desc \"group1\\ngroup2\"
#  ejabberdctl srg_user_add user host group grouphost
#   - add the JID user@host to the Shared Roster Group


import re           # regular expressions for string pattern matching

def convert_group_entry(input_line):
    input_list = re.split("\t", input_line)
    display = display_dict[input_list[0]]
    input_list[1] = re.sub("'", "", input_list[1])
    return "ejabberdctl srg_create '" + input_list[0] + "' jabber.rwth-aachen.de '" + input_list[0] + "' '" + input_list[1] + "' '" + display + "'\n"

def convert_group_member(input_line):
    input_list = re.split("\t", input_line)
    input_list[1] = re.sub(r'\s+$', '', input_list[1])
    return "ejabberdctl srg_user_add " + input_list[0] + " jabber.rwth-aachen.de '" + input_list[1] + "' jabber.rwth-aachen.de\n"


display_dict = {}
displays = open('from-openfire/group-displays.out', 'r')
for line in displays:
    splitline = re.split("\t", line)
    display_dict[splitline[0]] = re.sub(r'\s+$', '', splitline[1])
displays.close()
for key in display_dict:
    if display_dict[key] == "onlyGroup":
        display_dict[key] = key
    elif display_dict[key] == "nobody":
        display_dict[key] = ""

ejc = open('to-ejabberd/import3_group.sh', 'w')

ejc.write('#!/bin/sh -x\n')

f1 = open('from-openfire/groups.out', 'r')
for line in f1:
    group = re.split("\t", line)[0]
    grouplist = re.sub(r'\s+$', '', re.split("\t", line)[3])
    if grouplist != "":
        for entry in re.split(",", grouplist):
            if display_dict[entry] == "":
                display_dict[entry] = group
            else:
                display_dict[entry] = display_dict[entry] + "\\n" + group
f1.seek(0, 0)
for line in f1:
    group_entry = convert_group_entry(line)
    ejc.write(group_entry)
f1.close()

f2 = open('from-openfire/group-members.out', 'r')
for line in f2:
    group_entry = convert_group_member(line)
    ejc.write(group_entry)
f2.close()

ejc.close()
