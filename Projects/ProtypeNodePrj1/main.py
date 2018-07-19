########## This is the protype project for the node ##########
########## Author: Yunwei Jiang                     ##########
########## Date  : 2018-07-19                       ##########
import globalvar
import re
from network import LoRa
from network import Bluetooth
import socket
import machine
import time
import pycom
import _thread
import binascii
import struct
import config
#Global variables used in this file
BLEConnectionCounter = 0 # count the connection by clients
# Function testing

#Description: check if the BLE server is set up by another LoPy
#Note: for convention reason, the LoPy server name will be "LoPyServer"+device_id
def checkValidServer(server_name):
    if(server_name == None): return False
    else:
        #check if server_name contains "LoPyServer"
        if(re.match('LoPyServer*',server_name)):
            return True
        else:
            return False
    
#Description: Global varialbes test
def checkGlobalVar():
    print("The device id is ",globalvar.device_id)

#Global variable test2
outcount = 10
def GlobalVarTest():
    count = 10
    while(count>0): 
        count -= 1
        print(count)
#BLE client test
def BLEClientTest():
    bluetooth_client = Bluetooth()
    bluetooth_client.start_scan(-1)
    adv = bluetooth_client.get_adv()
    server_name = bluetooth_client.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)

#Testing program
'''
checkGlobalVar()
print(checkValidServer('LoPyServer'))
print(checkValidServer('LoPyServer11'))
print(checkValidServer('LoPyServeraa.ddd'))
print(checkValidServer('11LoPyServeraa.ddd'))

GlobalVarTest()
'''


################ BLE & LoRa Node ################
# This node will act as both BLE client and a   # 
# LoRa node device                              #
#################################################
def BLEServer():
    pycom.heartbeat(False)
    bluetooth = Bluetooth() #create a bluetooth object
    bluetooth.set_advertisement(name='LoPyServer'+str(globalvar.device_id), service_uuid=b'1111111111111111')
    
    #using callback conn_cb to check client's connection
    ##Function:   conn_cb(callback for bluetooth object events checking)
    ##Description:check there is any client connected to the service
    def conn_cb (bt_o):
        events = bt_o.events()#using events to check if there is any client connected to the service
        if  events & Bluetooth.CLIENT_CONNECTED:
            print("Client connected")
            pycom.rgbled(0x007f00) # green
        elif events & Bluetooth.CLIENT_DISCONNECTED:
            bt_o.disconnect_client()
            print("Client disconnected")
            pycom.rgbled(0x7f0000) # red           
    bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)
    bluetooth.advertise(True)
    #set up BLE service
    srv1 = bluetooth.service(uuid=b'1111111111111111', isprimary=True)
    #set up service character
    chr1 = srv1.characteristic(uuid=b'1111111111111111', value=5)
    #char1_read_counter = 0
    def char1_cb_handler(chr):
        #global char1_read_counter
        #char1_read_counter += 1
        global BLEConnectionCounter
        events = chr.events()
        if  events & Bluetooth.CHAR_WRITE_EVENT:
            print("Write request with value = {}".format(chr.value()))
        else:
            #modify here to send its device_id to other clients
            BLEConnectionCounter += 1
            p
            return str(globalvar.device_id)+' '+str(BLEConnectionCounter)
    #using the callback to send the data to other clients
    char1_cb = chr1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char1_cb_handler)

def BLEAndLoRaFun():
    ###### First, initialize as one LoRa node device ######
    # initialize LoRa in LORAWAN mode.
    # Please pick the region that matches where you are using the device:
    # Asia = LoRa.AS923
    # Australia = LoRa.AU915
    # Europe = LoRa.EU868
    # United States = LoRa.US915
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

    # create an ABP authentication params
    dev_addr = struct.unpack(">l", binascii.unhexlify('260214B3'))[0]
    nwk_swkey = binascii.unhexlify('2C2139EEC68B264BF1F0EDCE183CE33F')
    app_swkey = binascii.unhexlify('C25FB9A263307BF86B659298D86D4A45')

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
    '''
	###### Second, set up BLE server service ######
    pycom.heartbeat(False)
    bluetooth = Bluetooth() #create a bluetooth object
    bluetooth.set_advertisement(name='LoPyServer'+str(globalvar.device_id), service_uuid=b'1111111111111111')
    
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
    bluetooth.advertise(True)
    #set up BLE service
    srv1 = bluetooth.service(uuid=b'1111111111111111', isprimary=True)
    #set up service character
    chr1 = srv1.characteristic(uuid=b'1111111111111111', value=5)
    #char1_read_counter = 0
    def char1_cb_handler(chr):
        #global char1_read_counter
        #char1_read_counter += 1
        global BLEConnectionCounter
        events = chr.events()
        if  events & Bluetooth.CHAR_WRITE_EVENT:
            print("Write request with value = {}".format(chr.value()))
        else:
            #modify here to send its device_id to other clients
            BLEConnectionCounter += 1
            return str(globalvar.device_id)+' '+str(BLEConnectionCounter)
    #using the callback to send the data to other clients
    char1_cb = chr1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char1_cb_handler)
	'''
    ###### Third, set up BLE client service ######
    bluetooth_client = Bluetooth()
    bluetooth_client.start_scan(-1)
    #server_name1 = bluetooth_client.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
    
    counter = 50
    #while True:
    while counter > 0:
        
        #Gets an named tuple with the advertisement data received during the scanning. 
        #The structure is (mac, addr_type, adv_type, rssi, data)
        adv = bluetooth_client.get_adv()
        #servermac = ''#save the serer mac
        #use resolve_adv_data to resolve the 31 bytes of the advertisement message
        #Here is problem: when disconnect from server, then adv will always be null...

        #if get a valid advertisement from one server
        if adv:
            server_name = bluetooth_client.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
            #print(server_name)
            if checkValidServer(server_name):
                try:
                    #Opens a BLE connection with the device specified by the mac_addr argument
                    #This function blocks until the connection succeeds or fails.
                    #print(adv.mac)
                    #global servermac#change servermac to global
                    #servermac = adv.mac
                    #counter += 1
                    conn = bluetooth_client.connect(adv.mac)
                    #print('connected?',conn.isconnected())
                    services = conn.services()
                    #print('This is service',services)
                    #print(services)
                    #Yunwei - it seems that only when the type of uuid is bytes then could read the data from server
                    for service in services:
                        time.sleep(0.050)
                        if type(service.uuid()) == bytes:
                            chars = service.characteristics()
                            for char in chars:
                                #check if the character properties is PROP_READ
                                if (char.properties() & Bluetooth.PROP_READ):
                                    print('char {} value = {}'.format(char.uuid(), char.read()))
                                    counter -= 1
                                    #Use LoRa to send the data out
                                    s.send(char.read())
                                    time.sleep(4)
                    #Yunwei
                    conn.disconnect()
                    print('connected?',conn.isconnected())
                    #break
                    time.sleep(6)
                    bluetooth_client.start_scan(-1)
                except:
                    print("Error while connecting or reading from the BLE device")
                    #break
                    time.sleep(1)
                    bluetooth_client.start_scan(-1)
                    print('Scan again')

#Start this thread
print("Start work!")
#Start BLE server service
BLEServer()
#_thread.start_new_thread(BLEAndLoRaFun,())

