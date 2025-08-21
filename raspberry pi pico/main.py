import network
import socket
import time


SSID = "Cooperadora Profesores"
PASSWORD = "Profes_IMPA_2022"


estados = ["VERDE", "AMARILLO", "ROJO"]


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Conectando a WiFi...")
while not wlan.isconnected():
    time.sleep(1)
print("Conectado:", wlan.ifconfig())


UDP_IP = "192.168.1.50"  
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while True:
    for estado in estados:
        mensaje = estado.encode()
        sock.sendto(mensaje, (UDP_IP, UDP_PORT))
        print("Enviado:", estado)
        time.sleep(3)  

