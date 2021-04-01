import socket
import os
ludza={}
os.system('killall ttyd')
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('127.0.0.1',1062))
madport=1063
while True:
    usr,addr=s.recvfrom(1024)
    usr=usr.decode('utf-8')
    if usr in ludza:
            s.sendto(chr(ludza[usr]).encode('utf-8'),addr)
            continue
    madport+=1
    if os.fork()==0:
        os.system(f'ttyd -p {madport} nethack -u {usr}')
    else:
        ludza[usr]=madport
        s.sendto(chr(madport).encode('utf-8'),addr)
