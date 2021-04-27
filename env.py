# The code that runs on RPi
from __future__ import print_function
import urllib.request
from grovepi import *
from grove_rgb_lcd import *
import time
import paho.mqtt.publish as publish
import psutil
import string
import random

#TheThingSpeak
channelID = "xxxxxx"
writeAPIKey = "xxxx"
mqttHost = "mqtt.thingspeak.com"
mqttUsername = "xxxx"
mqttAPIKey = "ccccc"
tTransport = "websockets"
tPort = 80
topic = "channels/" + channelID + "/publish/" + writeAPIKey

#varipass.org
variID0="KeH4iWHr"
variKey="LTcMYOvAvDpfM5X8"
variID1="okUtEt4d"
variID2="PSWPd2kz"

setText("")
# There are 5 gas sensors
# MQ2 - Combustible Gas, Smoke
# MQ3 - Alcohol Vapor
# MQ5 - LPG, Natural Gas, Town Gas
# MQ9 - Carbon Monoxide, Coal Gas, Liquefied Gas
# O2 - Oxygen
gas_sensor = 0
pinMode(gas_sensor, "INPUT")
[temp, hum] = dht(5, 1)
t = str(temp)
h = str(hum)
sensor_value = analogRead(gas_sensor)
density = (int)(sensor_value / 1.024)
density = (float)(density/1000)
d = str(density)
setRGB(0, 255, 0)
setText_norefresh("T:" + t + "C " + "H: " + h + "%\nG: "+d+" "+time.strftime("%H:%M", time.localtime()))
#S = "<div class='col-lg-3 col-sm-6'><div class='small-box bg-green' id='total_queries' title='DHT'><div class='inner'><p>DHT</p><h3 class='statistic'><span id='dns_queries_today' class=''>"+t+"C / "+h+"% humidity</span></h3></div><div class='icon'><i class='ion ion-earth'></i></div></div></div>"
#f = open("/var/www/html/pihole/DHT.html", "w")
#f.write(S)
#f.close()
f = open("/var/www/html/dht.json", "w")
f.write('{"T":'+t+',"H":'+h+',"G":'+d+',"D":"???","HM":"'+time.strftime("%H:%M", time.localtime())+'"}')
f.close()
req="https://api.varipass.org/?action=write&id="+variID0+"&key="+variKey+"&value="+t
f = urllib.request.urlopen(req)
rslt=f.read().decode('utf-8')
#{"result":"success"}
print(req)
print(rslt)
time.sleep(1)
req="https://api.varipass.org/?action=write&id="+variID1+"&key="+variKey+"&value="+h
f = urllib.request.urlopen(req)
rslt=f.read().decode('utf-8')
#{"result":"success"}
#print(req)
#print(rslt)
density=int(density*1000)
d = str(density)
req="https://api.varipass.org/?action=write&id="+variID2+"&key="+variKey+"&value="+d
f = urllib.request.urlopen(req)
rslt=f.read().decode('utf-8')
time.sleep(3)

cpuPercent = psutil.cpu_percent(interval=1)
ramPercent = psutil.virtual_memory().percent
payload = "field1=" + str(cpuPercent) + "&field2=" + str(ramPercent) + "&field3=" + t + "&field4=" + h + "&field5=" + d
try:
  publish.single(topic, payload, hostname=mqttHost, transport=tTransport, port=tPort,auth={'username':mqttUsername,'password':mqttAPIKey})
  print (" Published CPU = ",cpuPercent," RAM = ", ramPercent," to host: " , mqttHost , " clientID= rpi00")
  #print (" payload:", payload)
except:
  print ("There was an error while publishing the data.")

time.sleep(3)
setRGB(0, 0, 0)
