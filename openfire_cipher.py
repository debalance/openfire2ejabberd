#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Encrypt and Decrypt Openfire passwords
Tested with data from Openfire 3.8.2 database
"""

__author__     = "Julien Lefeuvre"
__copyright__  = "Copyright 2013, Julien Lefeuvre"
__license__    = "CeCILL-B - http://www.cecill.info/licences.en.html"
__version__    = "1.0"
__maintainer__ = "Julien Lefeuvre"
__email__      = "julien.lefeuvre@inria.fr"
__status__     = "Production"
__date__       = "2013-07-04"

from Crypto.Cipher import Blowfish
from Crypto import Random
from struct import pack
import hashlib
from argparse import ArgumentParser
import os, sys, errno


def get_sha1(text):
  """return a SHA1 hash of the provided text"""
  m = hashlib.sha1()
  m.update(bytes(text))
  return m.digest()


def encrypt(password, key, cbciv=None):
  """return encrypted password (ciphertext)
       password: plaintext password
       key     : encoding key (passKey in Openfire DB)
       cbciv   : Blowfish initialization vector, optional, if none is provided
                 a random one will be generated"""

  # Openfire uses a sha1 hashed key as input for Blowfish-CBC
  sha1_key = bytes( get_sha1(key) )

  # blocksize (should be 8)
  bs       = Blowfish.block_size

  # generate a random cbciv or convert the on provided in hexadecimal in bytes
  # (Openfire provide the cbciv in hexadecimal in the first 16 chars of the
  # ciphertext)
  if not cbciv : cbciv = Random.new().read(bs)
  else: cbciv = cbciv.decode('hex')

  # pad the password to 8 bytes multiples - the password is encoded in utf-16BE
  plen = bs - divmod(len(password.encode('utf-16BE')),bs)[1]
  padding = [plen]*plen
  padding = pack('b'*plen, *padding)
  padded_password = bytes(password.encode('utf-16BE') + padding)

  # encrypt the password using Blowfish-CBC
  cipher = Blowfish.new(sha1_key, Blowfish.MODE_CBC, cbciv)
  ciphertext = cbciv + cipher.encrypt(padded_password)

  # return the ciphertext in hexadecimal as it is stored in Openfire DB
  return ciphertext.encode('hex')


def decrypt(ciphertext, key):
  """return decrypted password
       ciphertext: encrypted password
       key       : encoding key (passKey in Openfire DB)"""

  # Openfire uses a sha1 hashed key as input for Blowfish-CBC
  sha1_key = bytes( get_sha1(key) )

  # blocksize (should be 8)
  bs       = Blowfish.block_size

  # get the cbciv from the 8 first bytes of the ciphertext
  cbciv = ciphertext[:bs*2].decode('hex')

  # decrypt the padded password
  cipher = Blowfish.new(sha1_key, Blowfish.MODE_CBC, cbciv)
  encrypted_password = ciphertext[bs*2:].decode('hex')
  padded_password = cipher.decrypt(encrypted_password)

  # remove the padding at the end of the password
  npad = ord(padded_password[-1:])
  if npad < 9 :
    password_16b = padded_password[:-npad]
  else:
    password_16b = padded_password

  # remove utf-16BE encoding
  password = password_16b.decode('utf-16BE')
  return password


if __name__ == "__main__":

  parser = ArgumentParser(
    prog        = os.path.basename(__file__),
    description = __doc__,
    usage       = '%(prog)s enc -p <PASSWORD> -k <KEY> [-i <CBCIV>]\n'
                  '       %(prog)s dec -c <CIPHERTEXT> -k <KEY>',
  )
  parser.add_argument(
    'action',
    type = str,
    help = 'enc or dec to encrypt or decrypt',
  )
  parser.add_argument(
    '-k',
    '--key',
    type = str,
    help = 'Key used for encryption (for Openfire use 15 alphanumerics)'
           ' - OFPROPERTY.passwordKey in Openfire DB',
  )
  parser.add_argument(
    '-p',
    '--password',
    type = str,
    help = 'plaintext password used for encryption',
  )
  parser.add_argument(
    '-c',
    '--ciphertext',
    type = str,
    help = 'ciphertext to decrypt a password from (48 hex)',
  )
  parser.add_argument(
    '-i',
    '--cbciv',
    type = str,
    help = 'optional - Initialization Vector for CBC encryption (16 hex)',
  )

  args = parser.parse_args()

  # Process arguments
  if args.action == "enc":
    try:
      ciphertext = encrypt(
                     password = args.password,
                     key      = args.key,
                     cbciv    = args.cbciv,
                   )
      sys.stdout.write(ciphertext + "\n")
    except:
      sys.stderr.write("Error Processing arguments" + "\n")
      sys.exit(errno.EINVAL)

  elif args.action == "dec":
    try:
      password = decrypt(
                   ciphertext = args.ciphertext,
                   key      = args.key,
                   )
      sys.stdout.write(password + "\n")
    except:
      sys.stderr.write("Error Processing arguments" + "\n")
      sys.exit(errno.EINVAL)

  else:
    sys.stderr.write("Unknown action" + "\n")
    sys.exit(errno.EINVAL)

