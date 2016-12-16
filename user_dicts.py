#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re           # regular expressions for string pattern matching
import datetime     # for timestamp conversion

f = open('from-openfire/users.out', 'r')

user_email_dict = {}
user_reg_dict = {}
email_user_dict = {}
email_reg_dict = {}
for line in f:
    user = re.split("\t", line)[0]
    email = re.sub(r'\s+$', '', re.split("\t", line)[4])
    user_email_dict[user] = email
    reg = re.sub(r'\s+$', '', re.split("\t", line)[5])
    creationdate = datetime.datetime.fromtimestamp(int(reg)/1000.0)
    user_reg_dict[user] = creationdate
    email_user_dict[email] = user
    email_reg_dict[email] = creationdate

f.close()

#for key in user_email_dict:
#    print(key, user_email_dict[key], user_reg_dict[key])

f = open('invalid-emails.txt', 'r')
for line in f:
    mail = re.sub(r'\s+$', '', line)
    if not mail == "":
        if mail in email_reg_dict:
            print(str(email_user_dict[mail]))
f.close()
