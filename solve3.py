import socket
import re
import os
from Crypto.Util.strxor import strxor
import ast

HOST = "0.cloud.chals.io"
PORT = 33415


def get_value(s):
    match = re.search(r"'(.*)'", s)
    if match:
        return match.group(1)
    return None

def extract_bytes_literal(text):
    # Matches b'...' or b"...", including escaped quotes inside
    pattern = r"b(['\"])(?:\\.|(?!\1).)*\1"
    match = re.search(pattern, text, flags=re.DOTALL)
    if not match:
        return None
    
    literal = match.group(0)  # already a correct python bytes literal
    return ast.literal_eval(literal)

with socket.create_connection((HOST, PORT), timeout=10) as s:
    # استقبال أولي (مثلاً banner)
    data = s.recv(4096)
    
    res = data.decode(errors="replace")
    print(res)
    enc = get_value(res)
    
    encc = [enc[i:i+32] for i in range(0,len(enc),32)]
    print(encc)

    # إرسال رسالة (bytes)
    last=0
    for i in range(256):
        s.sendall(b"2\n")
        toxic = "00"*15 + hex(i)[2:].zfill(2) + "aa"*16 
        """
        trying to get a simple decryption block before the (xor phase in the cbc mode) let say "aa"*16
        it will be xord with the "00" block but the last byte is trying to bypass padding
        """
        data = s.recv(4096)
        res = data.decode(errors="replace")
        #print(res)
        
        s.sendall(toxic.encode() + b"\n")
        # لو الرد يحتوي على "something wrong" → كمّل اللوب
        data = s.recv(4096)
        res = data.decode(errors="replace")
        print(res)
        if b"something wrong" in data:
            continue

        # لو الرد *مافيهوش* "something wrong" → أوقف وطبع الرد
        print(f"[FOUND] Response: {i}\n", data.decode(errors="ignore"))
        last=i
        break
    pt = extract_bytes_literal(data.decode(errors="ignore"))
    pt = bytearray(pt)
    pt.append(last ^ 1)
    print(f"{pt=}, {len(pt)}")
    pt = pt[-16:]
    """
    After I got the simple "aa"*16 decryption block before the xor phase I make sure I appended the last missing byte that was missed because of the padding problem
    """
    
    for i in range(1000): # let say 1000
        s.sendall(b"2\n")
        rand = os.urandom(16).hex()
        toxic = "aa"*16 + rand
        """
        trying to decrypt the simple block "aa" with iv xored also with bypassing the padding randomly using random last cipher block
        """
        data = s.recv(4096)
        res = data.decode(errors="replace")
        #print(res)
        
        s.sendall(toxic.encode() + b"\n")
        # لو الرد يحتوي على "something wrong" → كمّل اللوب
        data = s.recv(4096)
        res = data.decode(errors="replace")
        print(res)
        if b"something wrong" in data:
            continue

        # لو الرد *مافيهوش* "something wrong" → أوقف وطبع الرد
        print(f"[FOUND] Response: {i}\n", data.decode(errors="ignore"))
        
        break

    """
    After I got the decryption response now I know that the 1st reselted block it will be the iv xored with "aa" block after the AES decryption
    """    

    ivpt = bytearray(extract_bytes_literal(data.decode(errors="ignore")))
    ivpt = ivpt[:16] # "aa" decryption block xored with iv 
    

    
    iv = strxor(ivpt, pt)
    print(f"{iv=}") # I found the iv
    

    for i in range(256):
        s.sendall(b"2\n")
        toxic = iv[:15].hex()+ hex(i)[2:].zfill(2) + encc[0]
        """
        try to decrypt 1st cipher block using placing it after the iv block but with last byte of iv changes to bypass the padding
        """
        data = s.recv(4096)
        res = data.decode(errors="replace")
        #print(res)
        
        s.sendall(toxic.encode() + b"\n")
        # لو الرد يحتوي على "something wrong" → كمّل اللوب
        data = s.recv(4096)
        res = data.decode(errors="replace")
        print(res)
        if b"something wrong" in data:
            continue

        # لو الرد *مافيهوش* "something wrong" → أوقف وطبع الرد
        print(f"[FOUND] Response: {i}\n", data.decode(errors="ignore"))
        
        """
        # if I got a response it will be like
        
        [FOUND] Response: 143
        pt = b'5\xce\xa8K\x86\x9d\xf7\xf8\xfea\xa15:\x0e\xc9=CyCTF{8817602d8'
        
        so I now know that
        
        last flag block = "4292afb5a3e3ae}\x01" 
        2nd flag block = "9c72ea815d3e34a?" 
        3rd flag block = "CyCTF{8817602d8?" 
        
        but I don't know the last '?' in 2nd and 3rd blocks because of the padding bypassing
        
        """
        break