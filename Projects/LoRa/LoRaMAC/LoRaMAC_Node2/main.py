import os
import socket
import time
import struct
from network import LoRa
from network import Bluetooth
import machine
import pycom
import _thread
import binascii
import struct
import gc
import re
#received data from BLE server
rec_msg = ''


#LoRa RAW part
def LoRaFun():
    # A basic package header, B: 1 byte for the deviceId, B: 1 bytes for the pkg size
    _LORA_PKG_FORMAT = "BB%ds"
    _LORA_PKG_ACK_FORMAT = "BBB"
    DEVICE_ID = 0x02
    global rec_msg

    # Open a Lora Socket, use tx_iq to avoid listening to our own messages
    # Please pick the region that matches where you are using the device:
    # Asia = LoRa.AS923
    # Australia = LoRa.AU915
    # Europe = LoRa.EU868
    # United States = LoRa.US915
    lora = LoRa(mode=LoRa.LORA, tx_iq=True, region=LoRa.US915)
    lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    lora_sock.setblocking(False)

    while(True):
        # Package send containing a simple string
        msg = "Device 2 meets Device "+rec_msg  
        pkg = struct.pack(_LORA_PKG_FORMAT % len(msg), DEVICE_ID, len(msg), msg)
        lora_sock.send(pkg)
            
        # Wait for the response from the gateway. NOTE: For this demo the device does an infinite loop for while waiting the response. Introduce a max_time_waiting for you application
        waiting_ack = True
        while(waiting_ack):
            recv_ack = lora_sock.recv(256)
            
            if (len(recv_ack) > 0):
                device_id, pkg_len, ack = struct.unpack(_LORA_PKG_ACK_FORMAT, recv_ack)
                if (device_id == DEVICE_ID):
                    if (ack == 200):
                        waiting_ack = False
                        # If the uart = machine.UART(0, 115200) and os.dupterm(uart) are set in the boot.py this print should appear in the serial port
                        print("ACK")
                    else:
                        waiting_ack = False
                        # If the uart = machine.UART(0, 115200) and os.dupterm(uart) are set in the boot.py this print should appear in the serial port
                        print("Message Failed")
        
        time.sleep(15)

#BLE client part
def BLEClient():
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
    
    global rec_msg
    ###### Third, set up BLE client service ######
    bluetooth_client = Bluetooth()
    bluetooth_client.start_scan(10)
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
                                    #create lora msg
                                    rec_msg = str(char.read())
                                    counter -= 1
                                    #Use LoRa to send the data out
                                    #s.send(char.read())
                                    time.sleep(5)                                
                    #Yunwei
                    conn.disconnect()
                    print('connected?',conn.isconnected())
                    #break
                    time.sleep(3)
                    gc.collect()
                    bluetooth_client.start_scan(10)
                except:
                    print("Error while connecting or reading from the BLE device")
                    #break
                    time.sleep(1)
                    if(bluetooth_client.isscanning()):
                        bluetooth_client.stop_scan()
                        bluetooth_client.deinit()
                        time.sleep(1)
                        bluetooth_client.init()
                        time.sleep(1)
                        #init again
                        #bluetooth_client.init(id=0, mode=Bluetooth.BLE, antenna=None)
                        bluetooth_client.start_scan(10)
                    else:
                        bluetooth_client.deinit()
                        time.sleep(1)
                        bluetooth_client.init()
                        time.sleep(1)
                        bluetooth_client.start_scan(10)
    bluetooth_client.stop_scan()
    bluetooth_client.deinit()

#Two thread:
_thread.start_new_thread(LoRaFun,())
_thread.start_new_thread(BLEClient,())

