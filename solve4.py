import socket
import re

HOST = "0.cloud.chals.io"
PORT = 33415
FLAG = "CyCTF{8817602d8?9c72ea815d3e34a?4292afb5a3e3ae}" # what I have form the FLAG
hexas = "123456789abcdef"

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
    print("")
        
        
    for i in hexas:
        s.sendall(b"1\n")
        
        data = s.recv(4096)
        res = data.decode(errors="replace")
        #print(res)

        s.sendall((FLAG[:15] + i).encode() + FLAG.encode()[16:32] + FLAG.encode()[32:48] + b"\n")
        data = s.recv(4096)
        res = data.decode(errors="replace")
        #print(res)
        ct = get_value(res)
        ctt = [ct[i:i+32] for i in range(0,len(ct),32)]
        #print(ctt)
        if ctt[0] == encc[0]:
            print("1st ? is: ", i)
            fst = i
            break
            
    for i in hexas:
        s.sendall(b"1\n")
        
        data = s.recv(4096)
        res = data.decode(errors="replace")
        #print(res)

        s.sendall((FLAG[:15] + fst).encode() + (FLAG[16:31] + i).encode() + FLAG.encode()[32:48] + b"\n")
        data = s.recv(4096)
        res = data.decode(errors="replace")
        #print(res)
        ct = get_value(res)
        ctt = [ct[i:i+32] for i in range(0,len(ct),32)]
        #print(ctt)
        if ctt[1] == encc[1]:
            print("2nd ? is: ", i)
            sst = i
            break
        
        """
        now this code is try to gessing the last hex charcter of each block in the flag 
        by re-encrypting the flag with trying all 16 possable hex digits in the last of each block
        
        # if I got a response it will be like
        
        1st ? is: 5
        2nd ? is: 4
        
        now the final flag is
        CyCTF{8817602d859c72ea815d3e34a44292afb5a3e3ae}
        
        thx for reading,
        wrote by: zeyad_0101
        
        email: zeyadsheeref@gmail.com
        """