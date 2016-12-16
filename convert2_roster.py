#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Relevant ejabberdctl commands:
#  ejabberdctl add_rosteritem localuser localserver user server nick group subscription
#   - add an item to a user's roster (supports ODBC)
#   - subscription is one of "none", "from", "to" or "both".


# From Openfire-openfire_3_9_1/src/java/org/jivesoftware/openfire/roster/RosterItem.java:
#
#    /**
#     * <p>Indicates the roster item should be removed.</p>
#     */
#    public static final SubType SUB_REMOVE = new SubType("remove", -1);
#    /**
#     * <p>No subscription is established.</p>
#     */
#    public static final SubType SUB_NONE = new SubType("none", 0);
#    /**
#     * <p>The roster owner has a subscription to the roster item's presence.</p>
#     */
#    public static final SubType SUB_TO = new SubType("to", 1);
#    /**
#     * <p>The roster item has a subscription to the roster owner's presence.</p>
#     */
#    public static final SubType SUB_FROM = new SubType("from", 2);
#    /**
#     * <p>The roster item and owner have a mutual subscription.</p>
#     */
#    public static final SubType SUB_BOTH = new SubType("both", 3);


import re           # regular expressions for string pattern matching

def convert_roster_entry(input_line):
    input_list = re.split("\t", input_line)
    if '@' not in input_list[1]:
        jid_list = ["", input_list[1]]
        #input_list[3] = "Non-User"
    else:
        jid_list = re.split('@', input_list[1])
    if ' ' in jid_list[0]:
        return "# invalid entry for " + input_list[0] + " skipped (space in localpart of JID): " + input_list[1] + "\n"
    if input_list[2] == "NULL":
        input_list[2] = input_list[1]
    elif input_list[2] == "":
        input_list[2] = input_list[1]
    else:
        input_list[2] = re.sub("'", "'\"'\"'", input_list[2])
    if input_list[3] == "NULL":
        input_list[3] = ""
    else:
        input_list[3] = re.sub("'", "'\"'\"'", input_list[3])
    sub = int(input_list[4])
    if sub == 0:
        subscription = "none"
    elif sub == 1:
        subscription = "to"
    elif sub == 2:
        subscription = "from"
    elif sub == 3:
        subscription = "both"
    else:
        return "# invalid entry skipped (sub != [0-3])\n"
    return "ejabberdctl add_rosteritem " + input_list[0] + " jabber.rwth-aachen.de '" + jid_list[0] + "' " + jid_list[1] + " '" + input_list[2] + "' '" + input_list[3] + "' " + subscription + '\n'


ejc = open('to-ejabberd/import2_roster.sh', 'w')

ejc.write('#!/bin/sh -x\n')

f = open('from-openfire/rosters.out', 'r')
for line in f:
    roster_entry = convert_roster_entry(line)
    ejc.write(roster_entry)
f.close()

ejc.close()
