

enc = 'ad82849d96d4b40ef692099f0a57ff62e259d46ea101e89d55d24938f92c7e58910cedf87f1e931d3cd7a1754d952191' #encrypted flag
encc = [enc[i:i+32] for i in range(0,len(enc),32)] # split the 3 cipher blocks

print(encc)
#toxic = encc[1][:14*2]+"aa"+encc[1][-1*2:]+encc[2]
toxic = encc[0][:15*2]+"aa"+encc[1] # first cipher block with last byte is anyhting to bypass the cheating detection
print(len(toxic))

print(toxic) # try decript this

"""
we got somthig like this
pt = b'5\xce\xa8K\x86\x9d\xf7\xf8\xfea\xa15:\x0e\xc9=4292afb5a3e3ae}'

so the last block with padding is
last flag block = "4292afb5a3e3ae}\x01"  

"""


"""

last block = "4292afb5a3e3ae}\x01"
2block = "9c72ea815d3e34a5"
1block = "CyCTF{8817602d84"

FLAG = "CyCTF{8817602d859c72ea815d3e34a44292afb5a3e3ae}"


toxicR = ""

[FOUND] Response: 143
 pt = b'5\xce\xa8K\x86\x9d\xf7\xf8\xfea\xa15:\x0e\xc9=9c72ea815d3e34a'
 
[FOUND] Response: 254
 pt = b'\xba\xe4\xabJ \xe9,\x84\xf1f\xdb\xb7-$\xc3\x879c72ea815d3e34a'

print(strxor(bytes.fromhex(toxicR[:2]), bytes.fromhex(toxic[2:])).hex())

"""