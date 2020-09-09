import struct
import crcmod
import db_dao

def check_error(header):
    crc16 = crcmod.predefined.Crc('x-25')
    Error_check=crc16.update(header[2:-4])
    crc=crc16.hexdigest()
    calculated_error=int(crc, 16)
    recieved_error=struct.unpack_from("!H",header[-4:-2])[0]
    if calculated_error==recieved_error:
        return 1
    return -1

def get_protocol(header):
    fields = struct.unpack_from("!HBB", header)
    is_correct=check_error(header)
    return fields[2]*is_correct

def get_imei(header):
    fields = struct.unpack_from("!HBBBBBBBBBB", header)
    imei=str(fields[3]%16)
    for i in range(4,11):
        imei=imei+str(fields[i]//16)+str(fields[i]%16)
    return imei

def read_location(header):
    fields = struct.unpack_from("!HBBBBBBBBBIIB", header)

    Date=str(2000+fields[3])+"-"+str(fields[4])+"-"+str(fields[5])+" "+str(fields[6])+":"+str(fields[7])+":"+str(fields[8]) #Date
    latitude=round(fields[10]/1800000,5) #latitude
    longitude=round(fields[11]/1800000,5) #longitude
    vitesse=fields[12] #vitesse

    seq=[latitude,longitude,vitesse,Date]
    return seq

def responde_message(header):
    protocol,serial=struct.unpack_from("!BH",header[3:4]+header[-6:-4])
    crc16 = crcmod.predefined.Crc('x-25')
    check=struct.pack('!BBH',5,protocol,serial)
    Error_check=crc16.update(check)
    crc=crc16.hexdigest()
    dat=struct.pack('!HBBHHH',0X7878,5,protocol,serial,int(crc, 16),0X0D0A)
    return dat
