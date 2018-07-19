########## This is for multiple thread test in LoPy ##########
########## Author: Yunwei Jiang                     ##########
########## Date  : 2018-07-13                       ##########
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
################ BLE & LoRa Node ################
# This node will act as both BLE client and a   # 
# LoRa node device                              #
#################################################
def BLEAndLoRaFun():
    #First, initialize as one LoRa node device
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
	
	
    #Second, act as BLE client
    bt = Bluetooth()
    bt.start_scan(-1)
    counter = 0
    while True:
        #Gets an named tuple with the advertisement data received during the scanning. 
        #The structure is (mac, addr_type, adv_type, rssi, data)
        adv = bt.get_adv()
        #servermac = ''#save the serer mac
        #use resolve_adv_data to resolve the 31 bytes of the advertisement message
        #Here is problem: when disconnect from server, then adv will always be null...
        if adv and bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == 'LoPyServer1':
            try:
                #Opens a BLE connection with the device specified by the mac_addr argument
                #This function blocks until the connection succeeds or fails.
                #print(adv.mac)
                #global servermac#change servermac to global
                #servermac = adv.mac
                counter += 1
                conn = bt.connect(adv.mac)
                #print('connected?',conn.isconnected())
                services = conn.services()
                #print('This is service',services)
                #print(services)
                '''
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
                '''
                #Yunwei - it seems that only when the type of uuid is bytes then could read the data from server
                for service in services:
                    time.sleep(0.050)
                    if type(service.uuid()) == bytes:
                        chars = service.characteristics()
                        for char in chars:
                            #check if the character properties is PROP_READ
                            if (char.properties() & Bluetooth.PROP_READ):
                                print('char {} value = {}'.format(char.uuid(), char.read())+str(counter))
                                #Use LoRa to send the data out
                                s.send(char.read())
                                time.sleep(4)
                #Yunwei
                conn.disconnect()
                print('connected?',conn.isconnected())
                #break
                time.sleep(6)
                bt.start_scan(-1)
            except:
                print("Error while connecting or reading from the BLE device")
                #break
                time.sleep(1)
                bt.start_scan(-1)
                print('Scan again')

#Start this thread
print("Start work!")
_thread.start_new_thread(BLEAndLoRaFun,())