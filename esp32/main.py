from rf_simple import Tx, Rx
from machine import Pin
import time
import random

tx_locomotora = Tx(20)
rx_estado = Rx(21)

VEL_MAXIMA = 120
ID_LOCOMOTORA = 7
NOMBRE_LOCOMOTORA = "PROTORP"

def recibir_estado():
    try:
        valor = rx_estado.listen()
        estados = {0: 'LIBRE', 1: 'PRECAUCION', 2: 'OCUPADO'}
        return estados.get(valor, 'DESCONOCIDO')
    except:
        return None

while True:
    velocidad_actual = random.randint(0, 150)
    estado = recibir_estado()

    if estado == 'OCUPADO':
        velocidad_actual = 0
    elif estado == 'PRECAUCION' and 110 <= velocidad_actual <= 120:
        velocidad_actual = 50
        

    velocidad_bits = min(int(velocidad_actual / 8), 15)
    byte = (velocidad_bits << 4) | ID_LOCOMOTORA
    tx_locomotora.send_byte(byte)

    print(f"{NOMBRE_LOCOMOTORA} , Estado recibido: {estado}, Velocidad: {velocidad_actual} km/h, Byte enviado: {byte}")
    time.sleep(2)

