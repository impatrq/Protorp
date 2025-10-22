from machine import Pin, PWM, UART
import bluetooth, time
import random 
from ble_simple_peripheral import BLESimplePeripheral 

PIN_ENA = 4
PIN_IN1 = 3
PIN_IN2 = 2

uart_rf = UART(1, baudrate=9600, tx=21, rx=20) 

pwm = PWM(Pin(PIN_ENA))
pwm.freq(1000) 

dir1 = Pin(PIN_IN1, Pin.OUT)
dir2 = Pin(PIN_IN2, Pin.OUT)

VEL_MAX_HARDWARE = 120
VEL_PRECAUCION_MIN = 110
ID_LOCO = 7
NOMBRE_LOCO = "PROTORP"

ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble, name=NOMBRE_LOCO)

vel_bt = None
estado_actual = "INICIANDO"
estado_seguridad = "LIBRE"

def set_motor_speed(vel):
    vel_abs = max(0, min(vel, VEL_MAX_HARDWARE)) if vel is not None else 0
    duty = int(vel_abs / VEL_MAX_HARDWARE * 65535) 
    
    if vel_abs == 0:
        dir1.value(0)
        dir2.value(0)
    else:
        dir1.value(1) 
        dir2.value(0) 
    
    pwm.duty_u16(duty)

def on_rx(data):
    global vel_bt, estado_seguridad
    try:
        new_vel = int(data.decode().strip())
        
        vel_bt = new_vel
        
        if vel_bt > VEL_MAX_HARDWARE:
            estado_seguridad = "OCUPADO"
        elif vel_bt >= VEL_PRECAUCION_MIN:
            estado_seguridad = "PRECAUCION"
        else:
            estado_seguridad = "LIBRE"
        
        print(f"Velocidad deseada (BLE): {vel_bt}")
        print(f"Estado de Seguridad Interna (BLE): {estado_seguridad}")

    except Exception as e:
        print(f"Error al procesar datos BLE: {e}")

sp.on_write(on_rx)

while True:
    if vel_bt is None:
        set_motor_speed(0)
        print("Esperando velocidad inicial por Bluetooth...")
        time.sleep(1)
        continue

    mensaje_tx = f"{ID_LOCO},{NOMBRE_LOCO},{vel_bt},{estado_seguridad}\n"
    try:
        uart_rf.write(mensaje_tx.encode('utf-8'))
    except Exception as e:
        print(f"Error UART TX: {e}")

    estado_bloqueo_uart = None
    if uart_rf.any():
        try:
            respuesta = uart_rf.readline().decode().strip()
            if respuesta in ["LIBRE", "PRECAUCION", "OCUPADO"]:
                estado_bloqueo_uart = respuesta
                estado_actual = estado_bloqueo_uart
                print(f"Estado de bloqueo REAL (UART): {estado_actual}")
        except Exception as e:
            pass
    
    if estado_bloqueo_uart is None:
        estado_actual = estado_seguridad

    vel_aplicada = min(vel_bt, VEL_MAX_HARDWARE)
    
    if estado_actual == "OCUPADO":
        vel_aplicada = 0
    elif estado_actual == "PRECAUCION":
        vel_aplicada = random.randint(50, 60)
    else:
        pass

    set_motor_speed(vel_aplicada)

    print(f"Motor | Estado Final: {estado_actual} | Deseada (BLE): {vel_bt} | Aplicada: {vel_aplicada}")
    
    time.sleep(0.5)





