'''
from network import LoRa
import socket
import binascii
import struct
import time

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN,region=LoRa.US915)

# create an ABP authentication params. Copy this from the TTN Device you created

dev_addr = struct.unpack(">l", binascii.unhexlify('26 02 1B 2A'.replace(' ','')))[0]#Device Address
#dev_addr = binascii.unhexlify('26 02 1B 2A'.replace(' ',''))#Device Address
nwk_swkey = binascii.unhexlify('7B374A79179E79DBB6ACB2B922D99333'.replace(' ',''))# Network Session Key
app_swkey = binascii.unhexlify('2480D39A06B5C2DF0AB6166FAA891DFF'.replace(' ',''))# App Session Key

for channel in range(0, 72):
   lora.remove_channel(channel)

# set the  channels  frequency
lora.add_channel(0, frequency=903900000, dr_min=0, dr_max=4)
# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# remove all the non-default channels
for i in range(1, 16):
    lora.remove_channel(i)


# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)# parameter changed from the original Code

# make the socket blocking
s.setblocking(False)

while True:
    #s.send(b'Hola LORAWAN')
    payload = b'\x00\x01\x02\x03'
    s.send(payload)
    #s.send(bytes([0xFF,0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]))#Send some sample Bytes
    print("packet send")
    # send the data
    
    time.sleep(4)
    time.sleep(4)
    time.sleep(4)
    time.sleep(4)
'''

#####ABP example#####
from network import LoRa
import socket
import binascii
import struct
import time
import config

# initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify('26021A14'))[0]
nwk_swkey = binascii.unhexlify('BB515D851353D2AB5ACCD112F0F2C597')
app_swkey = binascii.unhexlify('B74092CB7C5A79CAD681C384ABF925D2')

# remove all the channels
for channel in range(0, 72):
    lora.remove_channel(channel)

# set all channels to the same frequency (must be before sending the OTAA join request)
for channel in range(0, 72):
    lora.add_channel(channel, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=3)

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)# last parameter is 3 

# make the socket non-blocking
s.setblocking(False)

for i in range (200):
    pkt = b'PKT #' + bytes([i])
    print('Sending:', pkt)
    s.send(pkt)
    time.sleep(4)
    rx, port = s.recvfrom(256)
    if rx:
        print('Received: {}, on port: {}'.format(rx, port))
    time.sleep(6)


""" OTAA Node example compatible with the LoPy Nano Gateway """
'''
from network import LoRa
import socket
import binascii
import struct
import time
import config

# initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

# create an OTA authentication params
dev_eui = binascii.unhexlify('70B3D54999313D35')
app_eui = binascii.unhexlify('70B3D57ED0010707')
app_key = binascii.unhexlify('35612692F9AEB45035A26064BFDE910B')

# remove all the channels
for channel in range(0, 72):
    lora.remove_channel(channel)

# set all channels to the same frequency (must be before sending the OTAA join request)
#for channel in range(0, 72):
#   lora.add_channel(channel, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=3)
lora.add_channel(0, frequency=903900000, dr_min=0, dr_max=3)
# join a network using OTAA
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=4)

# wait until the module has joined the network
join_wait = 0
while True:
    time.sleep(2.5)
    if not lora.has_joined():
        print('Not joined yet...')
        join_wait += 1
        if join_wait == 5:
            lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=4)
            join_wait = 0
    else:
        break

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)

# make the socket non-blocking
s.setblocking(False)

time.sleep(5.0)

for i in range (200):
    pkt = b'PKT #' + bytes([i])
    print('Sending:', pkt)
    s.send(pkt)
    time.sleep(4)
    rx, port = s.recvfrom(256)
    if rx:
        print('Received: {}, on port: {}'.format(rx, port))
    time.sleep(6)
'''