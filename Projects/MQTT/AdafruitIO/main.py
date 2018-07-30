from mqtt import MQTTClient
from network import WLAN
import machine
import time

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
    print("Sending 111")
    client.publish(topic="Yunwei/feeds/lights", msg="111")
    time.sleep(5)
    print("Sending 222")
    client.publish(topic="Yunwei/feeds/lights", msg="222")
    client.check_msg()

    time.sleep(5)

