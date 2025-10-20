from machine import Pin, PWM
import time, random, bluetooth
from ble_simple_peripheral import BLESimplePeripheral
from rf_simple import Tx, Rx


ENA = PWM(Pin(4), freq=1000)   
IN1 = Pin(3, Pin.OUT)          
IN2 = Pin(2, Pin.OUT)          


tx = Tx(20)  
rx = Rx(21)  


ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble)

VEL_MAX = 120
ID_LOCOMOTORA = 7
NOMBRE = "PROTORP"

def set_motor_speed(vel):
    duty = int(min(max(vel, 0), VEL_MAX) / VEL_MAX * 1023)
    ENA.duty(duty)
    if vel > 0:
        IN1.value(1)
        IN2.value(0)
    else:
        IN1.value(0)
        IN2.value(0)

def recibir_estado():
    try:
        valor = rx.listen()
        estados = {0: 'LIBRE', 1: 'PRECAUCION', 2: 'OCUPADO'}
        return estados.get(valor, 'DESCONOCIDO')
    except:
        return None

velocidad = 0

while True:
    
    if sp.is_connected():
        data = sp.read()
        if data:
            cmd = data.decode().strip()
            if cmd == "STOP":
                velocidad = 0
            elif cmd.isdigit():
                velocidad = int(cmd)
    else:
        velocidad = random.randint(0, 150)

    estado = recibir_estado()
    if estado == 'OCUPADO':
        velocidad = 0
    elif estado == 'PRECAUCION' and velocidad > 80:
        velocidad = 50

    set_motor_speed(velocidad)


