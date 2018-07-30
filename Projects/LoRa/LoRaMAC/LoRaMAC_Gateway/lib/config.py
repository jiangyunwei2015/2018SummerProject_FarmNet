# wifi configuration
WIFI_SSID = 'LAPTOP-BHHF3UMN 4817'
WIFI_PASS = '3961516jim'

# AWS general configuration
AWS_PORT = 8883
AWS_HOST = 'a37un7oxgg9lwl.iot.us-west-2.amazonaws.com'
AWS_ROOT_CA = '/flash/cert/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem'
AWS_CLIENT_CERT = '/flash/cert/72b4829bc1-certificate.pem.crt'
AWS_PRIVATE_KEY = '/flash/cert/72b4829bc1-private.pem.key'

################## Subscribe / Publish client #################
#CLIENT_ID = 'iotconsole-1532455764891-6'
TOPIC = 'myLoPyTest'
OFFLINE_QUEUE_SIZE = -1
DRAINING_FREQ = 2
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5
LAST_WILL_TOPIC = 'PublishTopic'
LAST_WILL_MSG = 'To All: Last will message'

####################### Shadow updater ########################
#THING_NAME = "my thing name"
#CLIENT_ID = "ShadowUpdater"
#CONN_DISCONN_TIMEOUT = 10
#MQTT_OPER_TIMEOUT = 5

####################### Delta Listener ########################
#THING_NAME = "my thing name"
#CLIENT_ID = "DeltaListener"
#CONN_DISCONN_TIMEOUT = 10
#MQTT_OPER_TIMEOUT = 5

####################### Shadow Echo ########################
THING_NAME = "LoPyNode1"
CLIENT_ID = "arn:aws:iot:us-west-2:572965209519:thing/LoPyNode1"
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5