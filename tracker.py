import socket
from socket import error as SocketError
import errno
import decoder
import db_dao

#Function for handling connections. This will be used to create threads
def clientthread(client):
    login_protocol=0X1
    location_protocol=0X12
    heartbeat_protocol=0X13
    alarm_protocol=0X16
    imei="0"

    #infinite loop so that function do not terminate and thread do not end.
    while True:
        try:
            data = client.recv(1024)
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                print("error")
                raise
            break
        if not data:
            break
        if len(data)>9:
            protocol = decoder.get_protocol(data)

            if protocol==login_protocol:
                print("login message ", end='\n')
                imei = decoder.get_imei(data)
                reply = decoder.responde_message(data)
                client.sendall(reply)
                print("login response sent imei =",imei)

            elif protocol==location_protocol:
                print("location data ",end="\n")
                info=decoder.read_location(data)
                print("Date : ",info[3],"latitude : ",info[0],"longitude : ",info[1])
                db_dao.insert_data(imei , info[0],info[1],info[2],info[3] )

            elif protocol==alarm_protocol:
                print("alarm data ",end="\n")
                info=decoder.read_location(data)
                db_dao.insert_data(imei , info[0],info[1],info[2],info[3] )
                reply=decoder.respond_message(data)
                client.sendall(reply)
                print("Date : ",info[3],"latitude : ",info[1],"longitude : ",info[0])

            elif protocol==heartbeat_protocol:
                print("heartbeat",end="\n")
                reply = decoder.responde_message(data)
                client.sendall(reply)
                print ("heartbeat reponse sent" , end='\n')
            else:
                print(-protocol, end='\t')
                print('none of above',end='\n')

    print("connexion end")