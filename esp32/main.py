from rf_simple import Rx, Tx
from machine import Pin
import time


rx_via = 21        
tx_locomotora = 20  


ESTADOS = {
    0: 'LIBRE',
    1: 'PRECAUCION',
    2: 'OCUPADO'
}

NOMBRE_LOCOMOTORA = "PROTORP"
ID_LOCOMOTORA = 7



def recibir_estado():
    try:
        valor = rx_via.listen()
        estado = ESTADOS.get(valor, 'DESCONOCIDO')
        print("PROTORP recibió estado:", estado, f"({valor})")
        return estado
    except:
        print("Error de recepción")
        return None

def transmitir_respuesta(estado):
    if estado == 'LIBRE':
        velocidad_kmh = 120
    elif estado == 'PRECAUCION':
        velocidad_kmh = 50
    elif estado == 'OCUPADO':
        velocidad_kmh = 0
    else:
        velocidad_kmh = 0

    velocidad_bits = min(int(velocidad_kmh / 8), 15)  
    respuesta = (velocidad_bits << 4) | 7             
    tx_protorp.send_byte(respuesta)
    print(f"PROTORP,Velocidad={velocidad_kmh} km/h, ID=7, Byte={respuesta}")

while True:
    estado = recibir_estado()
    if estado in ESTADOS.values():
        transmitir_respuesta(estado)
    time.sleep(1)
