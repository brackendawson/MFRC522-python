#!/usr/bin/env python2

# read a tag secured with the well known keys

import sys, MFRC522, printdat

nfc = MFRC522.MFRC522()
#key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
key = [0x6B,0x65,0x79,0x20,0x61,0x00] # key a
#key = [0x6B,0x65,0x79,0x20,0x62,0x00] # key b

keyid = nfc.PICC_AUTHENT1A
#keyid = nfc.PICC_AUTHENT1B

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

for sector in [1,2]:
    status = nfc.Auth_Sector(keyid, sector, key, uid)
    if status != nfc.MI_OK:
        print "Authentication error"
        sys.exit()
    (status, data) = nfc.Read_Sector(sector)
    if status == nfc.MI_OK:
        printdat.printdat(data)
    else:
        print "Read error"
        sys.exit()

nfc.MFRC522_StopCrypto1()
