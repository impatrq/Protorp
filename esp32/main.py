from machine import Pin, PWM
import time, random
from rf_simple import Tx, Rx
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral


PIN_ENA = 4
PIN_IN1 = 3
PIN_IN2 = 2

pwm = PWM(Pin(PIN_ENA))
pwm.freq(1000)
dir1 = Pin(PIN_IN1, Pin.OUT)
dir2 = Pin(PIN_IN2, Pin.OUT)

tx= Tx(20)
rx= Rx(21)

VEL_MAX = 120
ID_LOCO = 7
NOMBRE_LOCO = "PROTORP"

ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble, name=NOMBRE_LOCO)

vel_bt = None

def set_motor_speed(vel):
    if vel < 0:
        vel = 0
    if vel > VEL_MAX:
        vel = VEL_MAX
    duty = int(vel / VEL_MAX * 65535)
    pwm.duty_u16(duty)
    dir1.value(1)
    dir2.value(0)

def recibir_estado():
    try:
        val = rx_estado.listen()
        estados = {0: 'LIBRE', 1: 'PRECAUCION', 2: 'OCUPADO'}
        return estados.get(val, 'DESCONOCIDO')
    except:
        return None

while True:
    if sp.is_connected():
        data = sp.read()
        if data:
            try:
                vel_bt = int(data.decode().strip())
            except:
                vel_bt = None
                
    if vel_bt is not None:
        velocidad_actual = vel_bt
    else:
        velocidad_actual = random.randint(50, 140)

    estado = recibir_estado()
    
    if estado == 'OCUPADO':
        velocidad_actual = 0
    elif estado == 'PRECAUCION' and velocidad_actual > 100:
        velocidad_actual = int(velocidad_actual / 2)

    set_motor_speed(velocidad_actual)

    velocidad_bits = min(int(velocidad_actual / 8), 15)
    byte = (velocidad_bits << 4) | ID_LOCO
    tx.send_byte(byte)

    print(f"{NOMBRE_LOCO}, Estado: {estado}, Vel: {velocidad_actual} km/h, Byte: {byte}")
    time.sleep(2)



