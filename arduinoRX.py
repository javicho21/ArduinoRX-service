from xbee import *
import binascii
import serial
import time
import paho.mqtt.client as paho
import datetime
import ssl


client = paho.Client()

# RaspberyPi conectado com Arduino usando modulo XBee na USB
ser = serial.Serial("/dev/ttyUSB0",19200)

xbee = ZigBee(ser)

time.sleep(2)

timezone = "Eastern/US"
state = "NY"
city = "New York"
burrough = "Manhattan"
lname = "Vazquez"
fname = "Javier"
customerId = "12345678"

RPIhostname = "node-R2"
RPIip = "192.168.0.103"

client.connect("iot.eclipse.org", 1883, 60)

#uncoment next line to activate user authentication
#client.username_pw_set("azhang","*********")

#uncoment next 2 lines for activate TLS
#client.tls_set("/etc/mosquitto/ca_certificates/ca.crt", certfile="/home/pi/myCA/client.crt", keyfile="/home/pi/myCA/client.key", cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
#client.connect("localhost", 8883, 60)

#coment next line if using TLS
client.connect("localhost", 1883, 60)

print "Waiting data from sensors ..."
#ser.write("sensors")

while (True):
   try:
	response = xbee.wait_read_frame()
#	print response

	remoteAddress = ((binascii.hexlify(response['source_addr_long'])))
	RxTAGs = response['rf_data']
        time_stamp = datetime.datetime.utcnow()
        time_stamp = time.time()
#        print RxTAGs
        mylist = RxTAGs.split(",")
        device = mylist[0]
        sensorName = mylist[1]
        sensorMetric = mylist[2]
        sensorUnit = mylist[3]
        sensorTimeStamp = int(mylist[4])*1000
	if sensorTimeStamp == 0:
		sensorTimeStamp = int(time_stamp)*1000
	  
        sensorValue = mylist[5]
	if mylist[6] == 'M':
		dataType = "METRIC" 
        elif mylist[6] == 'E':
		dataType = "EVENT"
#        msg ='{\nmetric: "%s",\ndatapoints: [\n{\ntags: {"arduino.name":"%s","rpi.hostname": "%s","rpi.ip": "%s","rpi.datatype": "%s", "sensor.name": "%s","sensor.unit": "%s"},\nvalues: {"%s":"%s"}\n}]\n}' % (sensorMetric,device,RPIhostname,RPIip,dataType,sensorName,sensorUnit,sensorTimeStamp,sensorValue)

	msg ='%s,arduino.name=%s,rpi.hostname=%s,rpi.datatype=%s,sensor.unit=%s,sensor.name=%s value=%s %s\n' % (sensorMetric,device,RPIhostname,dataType,sensorUnit,sensorName,sensorValue,sensorTimeStamp)
        
	print msg
        client.publish("javier/board1", msg)
        time.sleep(0.1)
	if dataType == "EVENT":
		client.publish("javier/board2", msg)
        	time.sleep(0.1)
   except KeyboardInterrupt:
	break

ser.close()

