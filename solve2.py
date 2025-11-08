import socket
import re

HOST = "0.cloud.chals.io"
PORT = 33415


def get_value(s):
    match = re.search(r"'(.*)'", s)
    if match:
        return match.group(1)
    return None


with socket.create_connection((HOST, PORT), timeout=10) as s:
    # استقبال أولي (مثلاً banner)
    data = s.recv(4096)
    
    res = data.decode(errors="replace")
    print(res)
    enc = get_value(res)
    
    encc = [enc[i:i+32] for i in range(0,len(enc),32)]
    print(encc)

    # إرسال رسالة (bytes)
    
    for i in range(256):
        s.sendall(b"2\n")
        """
        try to decrypt 2nd cipher block with keeping the 1st cipher block as same as but with trying all possible values of the last byte of it to bypass the padding
        """
        toxic = encc[0][:15*2] + hex(i)[2:].zfill(2) + encc[1]
        
        data = s.recv(4096)
        res = data.decode(errors="replace")
        #print(res)
        
        s.sendall(toxic.encode() + b"\n")
        data = s.recv(4096)
        res = data.decode(errors="replace")
        print(res)
        if b"something wrong" in data:
            continue

        print(f"[FOUND] Response: {i}\n", data.decode(errors="ignore")) 
        
        """
        # if I got a response it will be like
        
        [FOUND] Response: 143
        pt = b'5\xce\xa8K\x86\x9d\xf7\xf8\xfea\xa15:\x0e\xc9=9c72ea815d3e34a'
        
        so I now know that
        
        last flag block = "4292afb5a3e3ae}\x01" 
        2nd flag block = "9c72ea815d3e34a?" 
        
        but I don't know the last '?' because of the padding bypassing
        
        """
        break

