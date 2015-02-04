#!/usr/bin/env python2

import sys, MFRC522

nfc = MFRC522.MFRC522()
#key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF] # default
#key = [0x65,0x6B,0x20,0x79,0x00,0x61] # key a
key = [0x65,0x6B,0x20,0x79,0x00,0x62] # key b

#keyid = nfc.PICC_AUTHENT1A
keyid = nfc.PICC_AUTHENT1B

#data = [0x65, 0x48, 0x6c, 0x6c, 0x20, 0x6f, 0x6f, 0x57, 0x6c, 0x72, 0x0a, 0x64, 0, 0, 0, 0] #hello world
data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # zeros
#data = [0x65,0x6B,0x20,0x79,0x00,0x61,0x78,0x77,0x88,0x69,0x65,0x6B,0x20,0x79,0x00,0x62] # sector trailer for keyb=rw keya=ro
block = 4 #absolute block, not sector

print "Scan card..."

(status,TagType) = nfc.MFRC522_Request(nfc.PICC_REQIDL)
while status != nfc.MI_OK:
  (status,TagType) = nfc.MFRC522_Request(nfc.PICC_REQIDL)

(status,uid) = nfc.MFRC522_Anticoll()
if status != nfc.MI_OK:
  print "Failed to read UID"
  sys.exit()

print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
print uid
nfc.MFRC522_SelectTag(uid)

status = nfc.Auth_Block(keyid, block, key, uid)
if status != nfc.MI_OK:
  print "Authentication error"
  sys.exit()
(status, backData) = nfc.Write_Block(block, data)
if status == nfc.MI_OK:
  print "Data written"
else:
  print "Write error"
  sys.exit()

nfc.MFRC522_StopCrypto1()
