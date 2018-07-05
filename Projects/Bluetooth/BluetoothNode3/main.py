#This is the bluetooth client/central example for LoPy 
from network import Bluetooth
import time
bt = Bluetooth()
bt.start_scan(-1)
disconnetCount = 0
while True:  
  #bt = Bluetooth()
  #bt.start_scan(-1)
  adv = bt.get_adv()#get_adv:get 
  if adv:
      print("adv is not null")
      server = bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
      print(server)
  else:
      print("adv is null")

  if adv and bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == 'LoPyServer':
      try:
          conn = bt.connect(adv.mac)
          services = conn.services()
          print(services)
          for service in services:
              print(service.uuid())
              time.sleep(0.050)
              if type(service.uuid()) == bytes:
                  print('This is from COM4:Reading chars from service = {}'.format(service.uuid()))
              else:
                  print('This is from COM4:Reading chars from service = %x' % service.uuid())
              chars = service.characteristics()
              for char in chars:
                  if (char.properties() & Bluetooth.PROP_READ):
                      print('char {} value = {}'.format(char.uuid(), char.read()))
          conn.disconnect()
          time.sleep(1)
          #break
          print("Disconnected now!")
      except:
          print("Error while connecting or reading from the BLE device")
          break
          
  else:
      #time.sleep(0.050)
      print("Didn't connected!")
      time.sleep(1)
      