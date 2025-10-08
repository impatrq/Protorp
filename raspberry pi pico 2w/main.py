from rf_simple import Tx, Rx
from machine import Pin
import time


TX1_PIN = 0
RX1_PIN = 1


LED1 = {'ROJO': Pin(21, Pin.OUT), 'AMARILLO': Pin(20, Pin.OUT), 'VERDE': Pin(19, Pin.OUT)}
LED2 = {'ROJO': Pin(18, Pin.OUT), 'AMARILLO': Pin(17, Pin.OUT), 'VERDE': Pin(16, Pin.OUT)}


tx_via = Tx(TX1_PIN)
rx_locomotora = Rx(RX1_PIN)


ESTADOS = {
    'LIBRE': 0,
    'PRECAUCION': 1,
    'OCUPADO': 2
}

def transmitir_estado(nombre_estado):
    valor = ESTADOS[nombre_estado]
    tx_via.send_byte(valor)
    print(f"Transmitido estado de vía: {nombre_estado} → {valor}")

def actualizar_leds(nombre_estado):
    for color in LED1:
        LED1[color].value(0)
        LED2[color].value(0)

    if nombre_estado == 'LIBRE':
        LED1['VERDE'].value(1)
        LED2['VERDE'].value(1)
    elif nombre_estado == 'PRECAUCION':
        LED1['AMARILLO'].value(1)
        LED2['AMARILLO'].value(1)
    elif nombre_estado == 'OCUPADO':
        LED1['ROJO'].value(1)
        LED2['ROJO'].value(1)

def recibir_locomotora():
    try:
        valor = rx_locomotora.listen()
        print(f"Locomotora dice: {valor}")
    except:
        print("Error de recepción")


while True:
    estado_actual = 'LIBRE'  
    transmitir_estado(estado_actual)
    actualizar_leds(estado_actual)
    recibir_locomotora()
    time.sleep(1)