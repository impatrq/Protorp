from machine import Pin
from time import sleep

led_rojo = Pin(0, Pin.OUT)
led_amarillo = Pin(1, Pin.OUT)
led_verde = Pin(2, Pin.OUT)

def actualizar_semaforo(estado):
    if estado == "libre":
        led_rojo.value(0)
        led_amarillo.value(0)
        led_verde.value(1)
    elif estado == "precaucion":
        led_rojo.value(0)
        led_amarillo.value(1)
        led_verde.value(0)
    elif estado == "ocupada":
        led_rojo.value(1)
        led_amarillo.value(0)
        led_verde.value(0)

def leer_sensor():

    import random
    estados = ["libre", "precaucion", "ocupada"]
    return random.choice(estados)

while True:
    estado_via = leer_sensor()
    actualizar_semaforo(estado_via)
    print("Estado vía:", estado_via)
    sleep(1)
