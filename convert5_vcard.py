#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Relevant ejabberdctl commands:
#  set_vcard user host name content
#   - set content in a vCard field
#  set_vcard2 user host name subname content
#   - set content in a vCard subfield
#  set_vcard2_multi user host name subname contents
#   - set multiple contents in a vCard subfield

import re                           # regular expressions for string pattern matching
from xml.etree import ElementTree   # for processing XML

def process_node(user, node):
    name = re.sub("{vcard-temp}", "", node.tag)
    content = re.sub("'", "'\"'\"'", node.text)
    return "ejabberdctl set_vcard " + user + " jabber.rwth-aachen.de " + name + " '" + content + "'\n"

def process_children(user, node):
    name = re.sub("{vcard-temp}", "", node.tag)
    return_multi = []
    for child in node:
        subname = re.sub("{vcard-temp}", "", child.tag)
        if child.text is not None:
            child_text = re.sub("'", "'\"'\"'", child.text)
            return_multi += [ "ejabberdctl set_vcard2 " + user + " jabber.rwth-aachen.de " + name + " " + subname + " '" + child_text + "'\n" ]
    return return_multi

def convert_vcard(input_line):
    input_list = re.split("\t", input_line)
    try:
        root = ElementTree.fromstring(input_list[1])
        return_commands = []
        return_cmd = "# empty line\n"
        for name in root:
            if name.text is not None:
                return_cmd = process_node(input_list[0], name)
                return_commands.append(return_cmd)
            if len(list(name.iter())) > 1:
                return_commands += process_children(input_list[0], name)
        return return_commands
    except ElementTree.ParseError:
        print("IRRECOVERABLE PROBLEM in VCard of user " + input_list[0])
        return "# irrecoverable problem in vcard of user " + input_list[0] + "\n"


ejc = open('to-ejabberd/import5_vcard.sh', 'w')

ejc.write('#!/bin/sh -x\n')

f = open('from-openfire/vcards.out', 'r')
for line in f:
    commands = convert_vcard(line)
    for command in commands:
        ejc.write(command)
f.close()

ejc.close()
