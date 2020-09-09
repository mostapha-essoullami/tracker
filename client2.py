import socket
import crcmod
import struct
import random
from _thread import *


HOST = '104.43.201.167'  # The server's hostname or IP address
PORT = 8888       # The port used by the server
StartBit=30840
StopBit=3338

def calculecheckerror(msg):
    crc16 = crcmod.predefined.Crc('x-25')
    Error_check=crc16.update(msg)
    crc=crc16.hexdigest()
    return crc

def firstmsg():
    imie=random.sample(range(0, 9), 1)+random.sample(range(0, 99), 7)
    serial=1
    protool=1
    packet0=struct.pack('!HH',30840)
    packet1=struct.pack('!BBBBBBBBBBH',13,protocol,*[int(str(i),16) for i in imie],serial)
    Error_check=calculecheckerror(packet1)
    packet2=struct.pack('!HH',int(Error_check, 16),3338)
    return imie,packet0+packet1+packet2


def locationpacket(serial):
    protocol=0X12
    packet0=struct.pack('!HH',30840)
    Date_GPS=random.sample(range(0, 65535), 7)+random.sample(range(0,0XFF), 1)
    packet1=struct.pack('!BBIIIIIIHH',0X1F,protocol,*Date_GPS,serial)
    Error_check=calculecheckerror(packet1)
    packet2=struct.pack('!HH',int(Error_check, 16),3338)
    return Date_Gps,packet0+packet1+packet2

def heartbeatmsg(serial):
    protocol=0X13
    packet0=struct.pack('!HH',30840)
    heartorigin=random.sample(range(0,0XFF), 5)
    packet1=struct.pack('!BBBBBBBH',0X1F,protocol,*Date_GPS,serial)
    Error_check=calculecheckerror(packet1)
    packet2=struct.pack('!HH',int(Error_check, 16),3338)
    return hearorigin,packet0+packet1+packet2




def data_packet(serial,im):
    msg=struct.pack('!HBBBBBBBBBBHHH',StartBit,13,1,*[int(str(i),16) for i in im],serial,36061,StopBit)
    return msg

def location_data(serial):
    l=random.sample(range(0, 255), 16)
    a=struct.pack('!HBBBBBBBBBIIBHHBHBHHHH',StartBit,31,18,*l,serial,32897,StopBit)
    return a,l

def heartbeat(serial):
    l=random.sample(range(0, 255), 4)
    a=struct.pack('!HBBBBBHHHH',StartBit,31,19,*l,serial,32897,StopBit)
    return a,l

def f(i):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        serial=1
        imie= random.sample(range(0, 9), 1)+random.sample(range(0, 99), 7)
        msg=data_packet(serial,imie)
        s.sendall(msg)
        print(1)
        data1 = s.recv(1024)
        print(2)
        serial+=1

        locmsg,origin=location_data(serial)
        s.sendall(locmsg)
        print(3)
        serial+=1
        heartmsg,heartorg=heartbeat(serial)
        s.sendall(heartmsg)
        print(4)
        data2 = s.recv(1024)
        print(5)
for k in range(1):
    start_new_thread(f ,(11,))


##msg exemple
#msg exmple

#loginmsg=struct.pack('!HBBIIHHH',0X7878,0XD,1,0X1234567,0X89012345,1,0X8CDD,0XD0A)
#respondslogin=struct.pack('!HBBHHH',0X7878,5,1,1,0XD9DC,0XD0A)
#locationmsg=struct.pack('!HBBIHBIIBHHBHBHHHH',0X7878,0X1F,0X12,0XB081D11,0X2E10,0XCF,0X27AC7EB,0XC465849,0,0X148F,0X1CC,0,0X287D,0,0X1FB8,3,0X8081,0XD0A)
#heartbeatmsg=struct.pack('!HBBBBBHHHH',0X7878,8,0X13,0X4B,0X04,0X03,1,0X11,0X61F,0XD0A)
#respondsheartbit=struct.pack('!HBBHHH',0X7878,5,0X13,0X11,0XF970,0XD0A)
#s.sendall(loginmsg)
#print(1)
#logans = s.recv(1024)

#s.sendall(locationmsg)
#print(2)
#s.sendall(heartbeatmsg)
#print(3)
#heartans = s.recv(1024)