from network import LoRa
import socket
import machine
import time
from L76GNSV4 import L76GNSS
from pytrack import Pytrack

# initialize LoRa in LORA mode
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
# more params can also be given, like frequency, tx power and spreading factor
lora = LoRa(mode=LoRa.LORA, region=LoRa.US915)

# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

py = Pytrack()
L76 = L76GNSS(pytrack=py)
print("test L76 and LoRa")
#get GPS location message
print(L76.get_location())
# returns the info about sattelites in view at this moment
# even without the gps being fixed
#print(L76.gps_message('GSV'))

# returns the number of sattelites in view at this moment
# even without the gps being fixed
#print(L76.gps_message('GGA')['NumberOfSV'])

# returns the coordinates
# with debug true you see the messages parsed by the 
# library until you get a the gps is fixed
#print(L76.coordinates(debug=True))
#L76.getUTCDateTime(debug=True)
#L76._read_message(debug=True)

'''
while True:
    # send some data
    s.setblocking(True)
    s.send('Hello from Node1')

    # get any data received...
    s.setblocking(False)
    data = s.recv(64)
    print(data)

    # wait a random amount of time
    time.sleep(machine.rng() & 0x0F)
    '''
