import urequests as requests
import time
import machine
from machine import Pin, UART
import network
import json

SEGMENT_ID = 1

WIFI_SSID = "Cooperadora Profesores"
WIFI_PASSWORD = "Profes_IMPA_2022"

SERVER_IP = "192.168.1.138" 
SERVER_PORT = 5000
BASE_URL = f"http://{SERVER_IP}:{SERVER_PORT}"

PIN_SENSOR = 15

SEMAFORO_1 = {
    'ROJO': Pin(21, Pin.OUT), 
    'AMARILLO': Pin(20, Pin.OUT), 
    'VERDE': Pin(19, Pin.OUT)
}
SEMAFORO_2 = {
    'ROJO': Pin(18, Pin.OUT), 
    'AMARILLO': Pin(17, Pin.OUT), 
    'VERDE': Pin(16, Pin.OUT)
}

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
UARTS = [uart0, uart1]

sensor_ocupacion = Pin(PIN_SENSOR, Pin.IN, Pin.PULL_UP)
wlan = network.WLAN(network.STA_IF)

def connect_wifi():
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        max_wait = 10
        print(f"Intentando conectar a {WIFI_SSID}...")
        while max_wait > 0 and not wlan.isconnected():
            time.sleep(1)
            print('.', end='')
            max_wait -= 1

    if not wlan.isconnected():
        print("\n Conexión fallida. Reiniciando en 5s.")
        time.sleep(5)
        machine.reset()
    else:
        status = wlan.ifconfig()
        print("\n Conexión exitosa.")
        print('IP local:', status[0])

def get_loco_data():
    for uart in UARTS:
        if uart.any():
            try:
                line = uart.readline()
                if line:
                    data_str = line.decode('utf-8').strip()
                    data = json.loads(data_str)
                    loco_id = data.get('id', 0)
                    loco_speed = data.get('vel', 0)
                    print(f"  [UART Recibido en {uart.init(None)}] ID: {loco_id}, Vel: {loco_speed}")
                    return loco_id, loco_speed
            except Exception as e:
                print(f" Error al decodificar UART/JSON en {uart.init(None)}: {e}. Limpiando buffer.")
                while uart.any():
                    uart.read(1)
                time.sleep_ms(10)
    return 0, 0

def get_preceding_status(preceding_id):
    if preceding_id < 1:
        return "LIBRE"

    url = f"{BASE_URL}/get_segment_next_status/{preceding_id}"
    try:
        response = requests.get(url)
        status_next = response.json().get('status_next', 'LIBRE')
        response.close()
        return status_next
    except Exception as e:
        print(f" Error al consultar tramo anterior ({preceding_id}): {e}")
        return "LIBRE"

def send_update(status_real, status_next, loco_id, loco_speed):
    url = f"{BASE_URL}/update_segment"
    payload = {
        "segment_id": SEGMENT_ID,
        "status_real": status_real,
        "status_next": status_next,
        "loco_id": loco_id,
        "loco_speed": loco_speed,
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print(f"  [HTTP Enviado] Real: {status_real}, Next: {status_next}")
        else:
            print(f" Error Mímico ({response.status_code}): {response.text}")
        
        response.close()
        
    except Exception as e:
        print(f" Error de red HTTP al enviar estado: {e}")

def determine_security_status(status_real):
    if status_real == 'OCUPADO':
        return 'BLOQUEADO'
    else:
        return 'LIBRE'

def actualizar_semaforos(nombre_estado):
    for semaforo in [SEMAFORO_1, SEMAFORO_2]:
        semaforo['ROJO'].value(0)
        semaforo['AMARILLO'].value(0)
        semaforo['VERDE'].value(0)

        if nombre_estado == 'LIBRE':
            semaforo['VERDE'].value(1)
        elif nombre_estado == 'PRECAUCION':
            semaforo['AMARILLO'].value(1)
        elif nombre_estado == 'BLOQUEADO' or nombre_estado == 'OCUPADO':
            semaforo['ROJO'].value(1)

def main_loop():
    print(f"--- Tramo Fijo ID: {SEGMENT_ID} INICIADO ---")
    
    connect_wifi()
    
    preceding_id = SEGMENT_ID - 1
    
    while True:
        is_occupied = not sensor_ocupacion.value()
        status_real = 'OCUPADO' if is_occupied else 'LIBRE'
        
        loco_id, loco_speed = get_loco_data()
        
        preceding_status = get_preceding_status(preceding_id)
        
        status_next = determine_security_status(status_real)
        
        actualizar_semaforos(preceding_status)
        
        if loco_id != 0:
            signal_to_loco = json.dumps({"signal": preceding_status}) + "\n"
            for uart in UARTS:
                uart.write(signal_to_loco.encode('utf-8'))
            print(f"  [UART Enviado] Señal a Locomotora {loco_id} en ambos puertos: {preceding_status}")
        
        send_update(status_real, status_next, loco_id, loco_speed)

        time.sleep(0.5)

try:
    main_loop()
except Exception as e:
    print(f"FATAL ERROR en main_loop: {e}")
    time.sleep(5)
    machine.reset()


