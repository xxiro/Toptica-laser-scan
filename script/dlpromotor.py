# -*- coding: utf-8 -*-
"""
Control Motor of Toptica DL PRO 100

Adapted from http://ttdg.trinamic.com/viewtopic.php?f=13&t=2906
"""
#%%
import serial
port = "COM5"

#for the non 1218 dl pro it seems the minimum motor position is
#548000 1271.0454nm
#the max is 741000 1333.5128nm
#outside this range lasing stops
#in addition to the lookup table the motor will need fine adjustment due to it not being repeatable within the piezo tuning range

#for the 1218 dl pro
#max 494500 1254.3691
#min 181000 1135.3818


TMCL_cmd = {'ROR':   1,
        'ROL':   2,
        'MST':   3,
        'MVP':   4,
        'SAP':   5,
        'GAP':   6,
        'STAP':  7,
        'RSAP':  8,
        'SGP':   9,
        'GGP':  10,
        'STGP': 11,
        'RSGP': 12,
        'RFS':  13,
        'SIO':  14,
        'GIO':  15,
        'SCO':  30,
        'GCO':  31,
        'CCO':  32}

def SendCmd(address, command, cmd_type, motor, value):
    Tx = {}

    if value < 0:
        """ checks for negative numbers
    and converts them to appropriate value for
    the Trinamic control"""
        value += 4294967296
   
    Tx[0] = (address)
    Tx[1] = (TMCL_cmd[command])
    Tx[2] = (cmd_type)
    Tx[3] = (motor)
    hex_value = ('%08x' % value)
    #print("Hex value:", hex_value,"\n")
    Tx[4] = int(hex_value[0:2],16)
    Tx[5] = int(hex_value[2:4],16)
    Tx[6] = int(hex_value[4:6],16)
    Tx[7] = int(hex_value[6:],16)
    Tx[8] = 0
    i = 0
    cmd_array = []
    while i < 8:
        Tx[8] += Tx[i]
        cmd_array.append(Tx[i])
        #print('byte',i,'int',Tx[i],' Checksum:',Tx[8])
        i += 1
    Tx[8] = ("%08x" % Tx[8])
    #print('raw hex checksum:',Tx[8])
    Tx[8] = int(Tx[8][-2:],16)
    cmd_array.append(Tx[8])
    #print('hex checksum parsed int',Tx[8])
   
    i = 0
    ser = serial.Serial(port, 9600, 8, 'N', 1, 0.1)
    cmd_bytes = bytearray(cmd_array)
    #print(cmd_bytes)
    ser.write(cmd_bytes)
   
   
    reply = ser.read(9)
    #print('reply:',reply)
    print('reply:',"".join("\\x"+"%02x" % b for b in reply))
    addr,module,status,comnum=reply[0:4]
    if status!=100:
        raise ValueError("Communication failed, status Code: %d"%status)
    ser.close()
    return reply

#%%
def get_position():
    address = 1
    command = 'GAP'
    cmd_type = 1
    motor = 2
    value = 0
    rep=SendCmd(address, command, cmd_type, motor, value)
    pos=int.from_bytes(rep[4:8], byteorder='big', signed=False)
    return pos
    

    #%% test their example
    #int.from_bytes(b"\x00\x00\x02\xc7", byteorder='big', signed=False)

#%%
def set_position(pos):
    address = 1
    command = 'MVP'
    cmd_type = 0
    motor = 2
    value = pos
    SendCmd(address, command, cmd_type, motor, value)
