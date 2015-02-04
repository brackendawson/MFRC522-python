#!/usr/bin/env python2

import sys, MFRC522

nfc = MFRC522.MFRC522()
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

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

for x in range(16):
  status = nfc.Auth_Sector(nfc.PICC_AUTHENT1A, x, key, uid)
  if status != nfc.MI_OK:
    print "Authentication error"
    sys.exit()
  (status, data) = nfc.Read_Sector(x)
  if status == nfc.MI_OK:
    print data
  else:
    print "Read error"
    sys.exit()

nfc.MFRC522_StopCrypto1()
