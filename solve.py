enc = 'ad82849d96d4b40ef692099f0a57ff62e259d46ea101e89d55d24938f92c7e58910cedf87f1e931d3cd7a1754d952191' #encrypted flag
encc = [enc[i:i+32] for i in range(0,len(enc),32)] # split the 3 cipher blocks

print(encc)

toxic = encc[1][:15*2]+"aa"+encc[2] 
"""
try to decrypt the last cipher block with second cipher block before it with last byte is anyhting to bypass the cheating detection
"""

print(len(toxic))

print(toxic) # try decript this

"""
we got somthig like this
pt = b'5\xce\xa8K\x86\x9d\xf7\xf8\xfea\xa15:\x0e\xc9=4292afb5a3e3ae}'

so the last block with padding is
last flag block = "4292afb5a3e3ae}\x01"  

"""
