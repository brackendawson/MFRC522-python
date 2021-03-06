#!/usr/bin/env python2

#erase a tag initialised with well known keys

import sys, MFRC522

nfc = MFRC522.MFRC522()
#key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF] # default
#key = [0x6B,0x65,0x79,0x20,0x61,0x00] # key a
key = [0x6B,0x65,0x79,0x20,0x62,0x00] # key b

#keyid = nfc.PICC_AUTHENT1A
keyid = nfc.PICC_AUTHENT1B

#data = [0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x20, 0x57, 0x6f, 0x72, 0x6c, 0x64, 0x0a, 0, 0, 0, 0] #hello world
data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # zeros
trailer = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x07,0x80,0x69,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF] # default sector trailer
#data = [0x6B,0x65,0x79,0x20,0x61,0x00,0x78,0x77,0x88,0x69,0x6B,0x65,0x79,0x20,0x62,0x00] # sector trailer for keyb=rw keya=ro
#data = [0x6B,0x65,0x79,0x20,0x61,0x00,0x7F,0x07,0x88,0x69,0x6B,0x65,0x79,0x20,0x62,0x00] # sector trailer for keyb=rw d&a keya=rw d

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
    (status, backData) = nfc.Write_Block(sector * 4, data)
    if status != nfc.MI_OK:
        print "Write error"
        sys.exit()
    (status, backData) = nfc.Write_Block(sector * 4 + 1, data)
    if status != nfc.MI_OK:
        print "Write error"
        sys.exit()
    (status, backData) = nfc.Write_Block(sector * 4 + 2, data)
    if status != nfc.MI_OK:
        print "Write error"
        sys.exit()
    (status, backData) = nfc.Write_Block(sector * 4 + 3, trailer)
    if status != nfc.MI_OK:
        print "Write error"
        sys.exit()
    print "Data written"

nfc.MFRC522_StopCrypto1()
