#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Relevant ejabberdctl commands:
#  ejabberdctl register user host password  
#   - register a user


import re           # regular expressions for string pattern matching
import subprocess   # for executing external commands

def convert_user(input_line):
    input_list = re.split("\t", input_line)
    if input_list[1] == "NULL":
        input_list[1] = subprocess.getoutput('./openfire_cipher.py dec -k PutYourKeyHere -c ' + input_list[2])
    input_list[1] = re.sub("'", "'\"'\"'", input_list[1])
    return "ejabberdctl register " + input_list[0] + " jabber.rwth-aachen.de '" + input_list[1] + "'" + '\n'


ejc = open('to-ejabberd/import1_user.sh', 'w')

ejc.write('#!/bin/sh -x\n')

f = open('from-openfire/users.out', 'r')
for line in f:
    user = convert_user(line)
    ejc.write(user)
f.close()

ejc.close()
