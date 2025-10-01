import network
import time
import random
from umqttsimple import MQTTClient


ssid = 'Cooperadora Profesores'
password = 'Profes_IMPA_2022'

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("Cooperadora Profesores","Profes_IMPA_2022")

while not sta_if.isconnected():
    print("Conectando...")
    time.sleep(0.5)

print("Conectado:", sta_if.ifconfig())


client = MQTTClient("esp32", "broker.hivemq.com")
client.connect()


while True:
    velocidad = random.randint(0, 120)       
    voltaje = random.randint(160, 220)       
    temperatura = round(random.uniform(20.0, 40.0), 1)  

    mensaje = '{{"velocidad":{},"voltaje":{},"temperatura":{}}}'.format(velocidad, voltaje, temperatura)
    client.publish(b"protorp/tren", mensaje)
    print("Publicado:", mensaje)
    time.sleep(5)