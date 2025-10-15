from rf_simple import Tx, Rx
from machine import Pin
import time


rx_1 = Rx(1)
rx_2 = Rx(5)
tx_1 = Tx(0)
tx_2 = Tx(4)


SEMAFORO_1 = {'ROJO': Pin(21, Pin.OUT), 'AMARILLO': Pin(20, Pin.OUT), 'VERDE': Pin(19, Pin.OUT)}
SEMAFORO_2 = {'ROJO': Pin(18, Pin.OUT), 'AMARILLO': Pin(17, Pin.OUT), 'VERDE': Pin(16, Pin.OUT)}

VEL_MAXIMA = 120

def determinar_estado(velocidad):
    if velocidad > VEL_MAXIMA:
        return 2  
    elif 110 <= velocidad <= VEL_MAXIMA:
        return 1  
    else:
        return 0  

def actualizar_semaforos(estado):
    for color in SEMAFORO_1:
        SEMAFORO_1[color].value(0)
        SEMAFORO_2[color].value(0)
    if estado == 0:
        SEMAFORO_1['VERDE'].value(1)
        SEMAFORO_2['VERDE'].value(1)
    elif estado == 1:
        SEMAFORO_1['AMARILLO'].value(1)
        SEMAFORO_2['AMARILLO'].value(1)
    elif estado == 2:
        SEMAFORO_1['ROJO'].value(1)
        SEMAFORO_2['ROJO'].value(1)

def recibir_byte():
    for rx in [rx_1, rx_2]:
        try:
            valor = rx.listen()
            if valor != 0 and valor != 255:
                return valor
        except:
            pass
    return None

while True:
    byte_recibido = recibir_byte()
    if byte_recibido is not None:
        velocidad_bits = (byte_recibido >> 4) & 0x0F
        id_loco = byte_recibido & 0x0F
        velocidad_actual = velocidad_bits * 8
        estado = determinar_estado(velocidad_actual)
        actualizar_semaforos(estado)
        tx_1.send_byte(estado)
        tx_2.send_byte(estado)
        print(f"Tramo, Velocidad: {velocidad_actual} km/h, ID: {id_loco}, Byte recibido: {byte_recibido}, Estado transmitido: {estado}")
    time.sleep(2)
