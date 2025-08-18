from machine import Pin
from time import sleep
import random


led1_rojo = Pin(0, Pin.OUT)
led1_amarillo = Pin(1, Pin.OUT)
led1_verde = Pin(2, Pin.OUT)


led2_rojo = Pin(3, Pin.OUT)
led2_amarillo = Pin(4, Pin.OUT)
led2_verde = Pin(5, Pin.OUT)

def actualizar_semaforo(tramo, estado):
    if tramo == 1:
        leds = [led1_rojo, led1_amarillo, led1_verde]
    elif tramo == 2:
        leds = [led2_rojo, led2_amarillo, led2_verde]
    else:
        return

    if estado == "libre":
        leds[0].value(0)
        leds[1].value(0)
        leds[2].value(1)
    elif estado == "precaucion":
        leds[0].value(0)
        leds[1].value(1)
        leds[2].value(0)
    elif estado == "ocupada":
        leds[0].value(1)
        leds[1].value(0)
        leds[2].value(0)


def leer_sensor(tramo):
    estados = ["libre", "precaucion", "ocupada"]
    velocidad = random.randint(10, 50)  
    return random.choice(estados), velocidad


def controlar_tren(estado, velocidad, velocidad_max):
    if estado == "ocupada" or velocidad > velocidad_max:
        accion = "Frenar"
    elif estado == "precaucion":
        accion = "Reducir velocidad"
    else:
        accion = "Continuar"
    return accion


vel_max = 30  
while True:
    
    estado1, vel1 = leer_sensor(1)
    actualizar_semaforo(1, estado1)
    accion1 = controlar_tren(estado1, vel1, vel_max)
    
    
    estado2, vel2 = leer_sensor(2)
    actualizar_semaforo(2, estado2)
    accion2 = controlar_tren(estado2, vel2, vel_max)
    
    
    print(f"Tramo1: {estado1}, Vel={vel1} km/h -> {accion1}")
    print(f"Tramo2: {estado2}, Vel={vel2} km/h -> {accion2}")
    print("-"*30)
    
    sleep(1)

