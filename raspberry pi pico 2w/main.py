from machine import Pin, UART
import time, json, network, urequests

UART_ID = 15
UART_TX1 = 0
UART_RX1 = 1
UART_TX2 = 4
UART_RX2 = 5

uart_rf_1 = UART(0, baudrate=9600, tx=Pin(UART_TX1), rx=Pin(UART_RX1))
uart_rf_2 = UART(1, baudrate=9600, tx=Pin(UART_TX2), rx=Pin(UART_RX2))
uart_ports = [uart_rf_1, uart_rf_2]


PIN_R1 = 21     
PIN_A1 = 20
PIN_V1 = 19  

PIN_R2 = 18
PIN_A2 = 17
PIN_V2 = 16

led_R1, led_A1, led_V1 = Pin(PIN_R1, Pin.OUT), Pin(PIN_A1, Pin.OUT), Pin(PIN_V1, Pin.OUT)
led_R2, led_A2, led_V2 = Pin(PIN_R2, Pin.OUT), Pin(PIN_A2, Pin.OUT), Pin(PIN_V2, Pin.OUT)


WIFI_SSID = "Cooperadora Profesores"
WIFI_PASSWORD = "Profes_IMPA_2022"
SEGMENT_ID = 1
API_URL = "http://192.168.1.10/update_segment"

estado_real = "LIBRE"         
estado_siguiente = "LIBRE"    
locomotora_data = {"id": 0, "nombre": "", "velocidad": 0, "seguridad": "LIBRE"}
last_data_time = time.time()
TIMEOUT_SECS = 5

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Cooperadora Profesores","Profes_IMPA_2022")
    while not wlan.isconnected():
        time.sleep(1)
    print(f"[Wi-Fi] Conectado. IP: {wlan.ifconfig()[0]}")
    return wlan

def set_semaphore(leds, estado):
    r, a, v = leds
    r.value(0), a.value(0), v.value(0)
    
    if estado == "OCUPADO":
        r.value(1)
        print("Semaforo en ROJO (OCUPADO)")
    elif estado == "PRECAUCION":
        a.value(1)
        print("Semaforo en AMARILLO (PRECAUCION)")
    elif estado == "LIBRE":
        v.value(1)
        print("Semaforo en VERDE (LIBRE)")

def determine_real_state(loco_speed):
    global last_data_time
    
    if loco_speed > 0 and (time.time() - last_data_time) < TIMEOUT_SECS:
        return "OCUPADO"
    
    if loco_speed == 0 and (time.time() - last_data_time) < TIMEOUT_SECS:
        return "OCUPADO"
    
    return "LIBRE"

def apply_cascading_logic(current_state):
    if current_state == "OCUPADO":
        return "PRECAUCION"
    elif current_state == "PRECAUCION":
        return "LIBRE"
    return "LIBRE"

def send_web_status():
    try:
        payload = json.dumps({
            "segment_id": SEGMENT_ID,
            "status_real": estado_real,
            "status_next": estado_siguiente,
            "loco_id": locomotora_data["id"],
            "loco_speed": locomotora_data["velocidad"]
        })
        
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(API_URL, headers=headers, data=payload) 
        response.close()
        
    except Exception as e:
        print(f"[Web] Error al enviar estado: {e}")

if __name__ == '__main__':
    wlan = connect_wifi()
    set_semaphore((led_R1, led_A1, led_V1), "LIBRE")
    set_semaphore((led_R2, led_A2, led_V2), "LIBRE") 

    while True:
        
        for uart_rf in uart_ports:
            if uart_rf.any():
                try:
                    line = uart_rf.readline().decode().strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) == 4: 
                            locomotora_data["id"] = int(parts[0])
                            locomotora_data["nombre"] = parts[1]
                            locomotora_data["velocidad"] = int(parts[2])
                            locomotora_data["seguridad"] = parts[3] 
                            last_data_time = time.time()
                            
                            new_state = determine_real_state(locomotora_data["velocidad"])
                            
                            if new_state != estado_real:
                                estado_real = new_state
                                print(f"[Bloqueo] Tramo {SEGMENT_ID} REAL: {estado_real}")
                                
                                estado_siguiente = apply_cascading_logic(estado_real)
                                
                                uart_rf.write(f"{estado_real}\n".encode('utf-8'))
                                
                                set_semaphore((led_R1, led_A1, led_V1), estado_real)
                                set_semaphore((led_R2, led_A2, led_V2), estado_siguiente)

                except Exception as e:
                    print(f"[UART RX] Error de procesamiento: {e}")
        
        if wlan.isconnected():
            send_web_status()

        time.sleep(0.5)

