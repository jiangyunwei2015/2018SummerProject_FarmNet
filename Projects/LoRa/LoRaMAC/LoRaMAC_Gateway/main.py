#This is the example that using LoRaMAC nanogate, MQTT client to Adafruit IO broker project
#
from mqtt import MQTTClient
from network import WLAN
from network import LoRa
import machine
import time
import socket
import struct
import _thread
mqttmsg = ' '

def LoRaMACGateway():
    global mqttmsg
    #LoRaMAC gateway configuration begins
    # A basic package header, B: 1 byte for the deviceId, B: 1 byte for the pkg size, %ds: Formatted string for string
    _LORA_PKG_FORMAT = "!BB%ds"
    # A basic ack package, B: 1 byte for the deviceId, B: 1 byte for the pkg size, B: 1 byte for the Ok (200) or error messages
    _LORA_PKG_ACK_FORMAT = "BBB"

    # Open a LoRa Socket, use rx_iq to avoid listening to our own messages
    # Please pick the region that matches where you are using the device:
    # Asia = LoRa.AS923
    # Australia = LoRa.AU915
    # Europe = LoRa.EU868
    # United States = LoRa.US915
    lora = LoRa(mode=LoRa.LORA, rx_iq=True, region=LoRa.US915)
    lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    lora_sock.setblocking(False)

    while True:
        recv_pkg = lora_sock.recv(512)
        if (len(recv_pkg) > 2):
            recv_pkg_len = recv_pkg[1]

            device_id, pkg_len, message = struct.unpack(_LORA_PKG_FORMAT % recv_pkg_len, recv_pkg)
    # If the uart = machine.UART(0, 115200) and os.dupterm(uart) are set in the boot.py this print should appear in the serial port
            print('Device: %d - Pkg:  %s' % (device_id, message))
            mqttmsg = str(message)
            ack_pkg = struct.pack(_LORA_PKG_ACK_FORMAT, device_id, 1, 200)
            lora_sock.send(ack_pkg)  



def MQTTClientInit():
    global mqttmsg
    # wifi configuration
    WIFI_SSID = 'LAPTOP-BHHF3UMN 4817'
    WIFI_PASS = '3961516jim'
    def sub_cb(topic, msg):
        print(msg)
    

    wlan = WLAN(mode=WLAN.STA)
    wlan.connect(WIFI_SSID, auth=(WLAN.WPA2, WIFI_PASS), timeout=5000)

    while not wlan.isconnected():  
        machine.idle()
    print("Connected to WiFi\n")

    client = MQTTClient("lights11", "io.adafruit.com",user="Yunwei", password="c50a57f98bf34cb3ae5d6a3b124a1551", port=1883)

    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic="Yunwei/feeds/lights")

    while True:
        print("Sending "+mqttmsg)
        client.publish(topic="Yunwei/feeds/lights", msg=mqttmsg)
        time.sleep(5)
        #print("Sending 222")
        #client.publish(topic="Yunwei/feeds/lights", msg=mqttmsg)
        client.check_msg()
        time.sleep(5)

#Two thread:
_thread.start_new_thread(LoRaMACGateway,())
_thread.start_new_thread(MQTTClientInit,())