#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Relevant ejabberdctl commands:
#  ejabberdctl private_set user host element 
#   - set element to the user private storage


import re           # regular expressions for string pattern matching

def convert_private_storage(input_line):
    input_list = re.split("\t", input_line)
    input_list[1] = re.sub("'", "'\"'\"'", input_list[1])
    return "ejabberdctl private_set " + input_list[0] + " jabber.rwth-aachen.de '" + input_list[1] + "'\n"


ejc = open('to-ejabberd/import6_private.sh', 'w')

ejc.write('#!/bin/sh -x\n')

f = open('from-openfire/private.out', 'r')
for line in f:
    private_storage = convert_private_storage(line)
    ejc.write(private_storage)
f.close()

ejc.close()
