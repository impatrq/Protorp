from rf_simple import Rx, Tx
from machine import Pin
import time


RX_PIN = 21  
TX_PIN = 20 


rx_via = Rx(RX_PIN)
tx_locomotora = Tx(TX_PIN)  


ESTADOS = {
    0: 'LIBRE',
    1: 'PRECAUCION',
    2: 'OCUPADO'
}


VELOCIDAD = 3  
ID_LOCO = 7    

def recibir_estado():
    try:
        valor = rx_via.listen()
        estado = ESTADOS.get(valor, 'DESCONOCIDO')
        print(f"Estado recibido: {estado} ({valor})")
        return estado
    except:
        print("Error de recepción")
        return None

def transmitir_respuesta():
    
    respuesta = (VELOCIDAD << 4) | ID_LOCO  
    tx_locomotora.send_byte(respuesta)
    print(f"Respuesta enviada: velocidad={VELOCIDAD}, ID={ID_LOCO}, byte={respuesta}")


while True:
    estado = recibir_estado()
    if estado:
        transmitir_respuesta()  
    time.sleep(1)