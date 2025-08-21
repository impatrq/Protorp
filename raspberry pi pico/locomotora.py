import network
import socket
import time
from machine import Pin


SSID = "Cooperadora Profesores"
PASSWORD = "Profes_IMPA_2022"

led = Pin("LED", Pin.OUT)


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Conectando a WiFi...")
while not wlan.isconnected():
    time.sleep(1)
print("Conectado:", wlan.ifconfig())

UDP_IP = "0.0.0.0"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Esperando datos...")

while True:
    data, addr = sock.recvfrom(1024)
    estado = data.decode()
    print("Recibido:", estado)

    if estado == "VERDE":
        led.on()
    elif estado == "AMARILLO":
        for _ in range(3):
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.5)
    elif estado == "ROJO":
        for _ in range(5):
            led.on()
            time.sleep(0.2)
            led.off()
            time.sleep(0.2)
