#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Relevant ejabberdctl commands:
#  ejabberdctl privacy_set user host xmlquery 
#   - send an IQ set privacy stanza for a local account


import re           # regular expressions for string pattern matching

def convert_privacy_list(input_line):
    input_list = re.split("\t", input_line)
    input_list[1] = re.sub("'", "'\"'\"'", input_list[1])
    return "ejabberdctl privacy_set " + input_list[0] + " jabber.rwth-aachen.de '" + input_list[1] + "'\n"

ejc = open('to-ejabberd/import7_privacy.sh', 'w')

ejc.write('#!/bin/sh -x\n')

f = open('from-openfire/privacy.out', 'r')
for line in f:
    privacy_list = convert_privacy_list(line)
    ejc.write(privacy_list)
f.close()

ejc.close()
