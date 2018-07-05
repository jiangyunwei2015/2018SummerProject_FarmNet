#This is the bluetooth client/central example for LoPy 
from network import LoRa
import socket
import machine
from network import Bluetooth
import time
import pycom
import _thread
################ BLE Part ################
# This node will act as both BLE server  # 
# and client itself                      #
##########################################
def BlueToothFun():
    #Also act as a server
    pycom.heartbeat(False)
    bluetooth = Bluetooth() #create a bluetooth object
    bluetooth.set_advertisement(name='LoPyServer1', service_uuid=b'1234567890123456')
    #id for this device 
    deviceID = 888
    #using callback conn_cb to check client's connection

    ##Function:   conn_cb(callback for bluetooth object events checking)
    ##Description:check there is any client connected to the service

    def conn_cb (bt_o):
        events = bt_o.events()#using events to check if there is any client connected to the service
        if  events & Bluetooth.CLIENT_CONNECTED:
            print("Client connected")
            pycom.rgbled(0x007f00) # green
        elif events & Bluetooth.CLIENT_DISCONNECTED:
            print("Client disconnected")
            pycom.rgbled(0x7f0000) # red
            
    bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)
    #
    bluetooth.advertise(True)

    srv1 = bluetooth.service(uuid=b'1234567890123456', isprimary=True)

    chr1 = srv1.characteristic(uuid=b'ab34567890123456', value=5)

    char1_read_counter = 0

    def char1_cb_handler(chr):
        global char1_read_counter
        char1_read_counter += 1

        events = chr.events()
        if  events & Bluetooth.CHAR_WRITE_EVENT:
            print("Write request with value = {}".format(chr.value()))
        else:
            #modify here to send message to other clients
            return str(deviceID)+' '+str(char1_read_counter)
    #using the callback to send the data to other clients
    char1_cb = chr1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char1_cb_handler)

    srv2 = bluetooth.service(uuid=1234, isprimary=True)

    chr2 = srv2.characteristic(uuid=4567, value=0x1234)
    char2_read_counter = 0xF0
    def char2_cb_handler(chr):
        global char2_read_counter
        char2_read_counter += 1
        if char2_read_counter > 0xF1:
            return char2_read_counter

    char2_cb = chr2.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=char2_cb_handler)


    bt = Bluetooth()
    bt.start_scan(-1)
    while True:
        #Gets an named tuple with the advertisement data received during the scanning. 
        #The structure is (mac, addr_type, adv_type, rssi, data)
        adv = bt.get_adv()
        #servermac = ''#save the serer mac
        #use resolve_adv_data to resolve the 31 bytes of the advertisement message
        if adv and bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == 'LoPyServer2':
            try:
                #Opens a BLE connection with the device specified by the mac_addr argument
                #This function blocks until the connection succeeds or fails.
                #print(adv.mac)
                #global servermac#change servermac to global
                #servermac = adv.mac
                conn = bt.connect(adv.mac)
                print('connected?',conn.isconnected())
                services = conn.services()
                print('This is service',services)
                #print(services)
                for service in services:
                    print('This is service uuid',service.uuid())
                    time.sleep(0.050)
                    if type(service.uuid()) == bytes:
                        print('if bytes:Reading chars from service = {}'.format(service.uuid()))
                    else:
                        print('if not bytes:Reading chars from service = %x' % service.uuid())
                    chars = service.characteristics()
                    for char in chars:
                        if (char.properties() & Bluetooth.PROP_READ):
                            print('char {} value = {}'.format(char.uuid(), char.read()))
                conn.disconnect()
                print('connected?',conn.isconnected())
                break
            except:
                print("Error while connecting or reading from the BLE device")
                break



################ LoRa Part ################
# This node will also act as LoRa gateway # 
# that would receive the data from nodes  #
###########################################
def LoRaFun():
    lora = LoRa(mode=LoRa.LORA, region=LoRa.US915)
    # create a raw LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
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

#Start these two threads
print("Start work!")
_thread.start_new_thread(BlueToothFun,())
_thread.start_new_thread(LoRaFun,())
