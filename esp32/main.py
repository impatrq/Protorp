import time
from machine import Pin, PWM, UART
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral

PIN_ENA = 4
PIN_IN1 = 3
PIN_IN2 = 2

pwm = PWM(Pin(PIN_ENA))
pwm.freq(1000)
dir1 = Pin(PIN_IN1, Pin.OUT)
dir2 = Pin(PIN_IN2, Pin.OUT)

PWM_MIN_IMPULSO = 30
VEL_MAX_HARDWARE = 100

uart_loc = UART(1, baudrate=115200, tx=Pin(21), rx=Pin(20))

ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble, name="PROTORP")

vel_deseada = 0
velocidad_actual = 50
direccion = 1
senal_seguridad = 'C'

def set_motor_speed(vel):
    vel_abs = abs(vel)
    if vel > 0:
        dir1.value(1)
        dir2.value(0)
    elif vel < 0:
        dir1.value(0)
        dir2.value(1)
    else:
        dir1.value(0)
        dir2.value(0)
        pwm.duty(0)
        return

    if vel_abs > 0 and vel_abs < PWM_MIN_IMPULSO:
        vel_a_usar = PWM_MIN_IMPULSO
    else:
        vel_a_usar = vel_abs

    duty = int(min(vel_a_usar, VEL_MAX_HARDWARE) * 1023 / 100)
    pwm.duty(duty)

def on_rx(data):
    global vel_deseada, direccion, velocidad_actual
    try:
        message = data.decode().strip()
        print(f"Comando: {message}")
        
        if message == 'F':
            direccion = 1
            vel_deseada = velocidad_actual
            print("Adelante")
        elif message == 'B':
            direccion = -1
            vel_deseada = -velocidad_actual
            print("Atras")
        elif message == 'S':
            vel_deseada = 0
            print("Stop")
        elif message.isdigit():
            speed_val = int(message)
            if 0 <= speed_val <= 100:
                velocidad_actual = speed_val
                vel_deseada = speed_val * direccion
                print(f"Velocidad: {speed_val}%")
                
    except Exception as e:
        print(f"Error: {e}")

sp.on_write(on_rx)

def receive_security_signal():
    global senal_seguridad
    if uart_loc.any():
        try:
            data = uart_loc.readline()
            if data:
                signal = data.decode('utf-8').strip()
                if signal in ('A', 'B', 'C'):
                    senal_seguridad = signal
        except:
            pass

def send_speed_to_raspberry():
    mensaje = f"{vel_deseada}\n"
    try:
        uart_loc.write(mensaje.encode('utf-8'))
    except:
        pass

print("PROTORP INICIADO")

while True:
    receive_security_signal()
    send_speed_to_raspberry()
    
    if senal_seguridad == 'A':
        vel_aplicada = 0
        estado = "ROJO"
    elif senal_seguridad == 'B':
        vel_limit = 30
        if abs(vel_deseada) > vel_limit:
            vel_aplicada = int((vel_deseada / abs(vel_deseada)) * vel_limit)
        else:
            vel_aplicada = vel_deseada
        estado = "AMARILLO"
    else:
        vel_aplicada = vel_deseada
        estado = "VERDE"

    set_motor_speed(vel_aplicada)
    print(f"Estado: {estado} | Vel: {vel_deseada} | Motor: {vel_aplicada}")
    time.sleep_ms(1000)






