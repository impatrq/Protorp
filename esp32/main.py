from machine import Pin, PWM
import time, random
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral

PIN_ENA = 4
PIN_IN1 = 3
PIN_IN2 = 2

pwm = PWM(Pin(PIN_ENA))
pwm.freq(1000)
dir1 = Pin(PIN_IN1, Pin.OUT)
dir2 = Pin(PIN_IN2, Pin.OUT)

VEL_MAX = 120
ID_LOCO = 7
NOMBRE_LOCO = "PROTORP"

ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble, name=NOMBRE_LOCO)

vel_bt = None
estado = "LIBRE"

def set_motor_speed(vel):
    if vel < 0:
        vel = 0
    if vel > VEL_MAX:
        vel = VEL_MAX
    duty = int(vel / VEL_MAX * 65535)
    pwm.duty_u16(duty)
    dir1.value(1)
    dir2.value(0)

def on_rx(data):
    global vel_bt
    try:
        vel_bt = int(data.decode().strip())
        print("Velocidad recibida por BLE:", vel_bt)
    except:
        vel_bt = None

sp.on_write(on_rx)

while True:
    if vel_bt is not None:
        velocidad_actual = vel_bt
    else:
        velocidad_actual = random.randint(50, 140)

    if velocidad_actual > 120:
        estado = "OCUPADO"
    elif velocidad_actual >= 100:
        estado = "PRECAUCION"
    else:
        estado = "LIBRE"

    if estado == "OCUPADO":
        velocidad_actual = 0
    elif estado == "PRECAUCION" and velocidad_actual > 100:
        velocidad_actual = int(velocidad_actual / 2)

    set_motor_speed(velocidad_actual)

    mensaje = f"{estado}:{velocidad_actual}"
    try:
        sp.send(mensaje)
    except:
        pass

    print(f"{NOMBRE_LOCO} | Estado: {estado} | Vel: {velocidad_actual} km/h")
    time.sleep(1)




