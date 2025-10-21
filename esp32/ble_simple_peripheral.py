import bluetooth
import time
from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX   = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_NOTIFY,)
_UART_RX   = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_WRITE,)
_UART_SERVICE = (_UART_UUID, (_UART_TX, _UART_RX,),)

class BLESimplePeripheral:
    def __init__(self, ble, name="PROTORP"):
        self._ble = ble
        self._name = name
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._connections = set()
        self._rx_buffer = bytearray()
        time.sleep_ms(50)
        self._advertise(self._name)
        print("[BLE] Iniciado, handles tx:", self._tx_handle, "rx:", self._rx_handle)

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, addr_type, addr = data
            self._connections.add(conn_handle)
            print("[BLE] Conectado:", conn_handle, addr_type, bytes(addr))
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, addr_type, addr = data
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            print("[BLE] Desconectado:", conn_handle)
            time.sleep_ms(50)
            self._advertise(self._name)
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            if value_handle == self._rx_handle:
                val = self._ble.gatts_read(self._rx_handle)
                self._rx_buffer += val
                print("[BLE] WRITE desde conn", conn_handle, "->", val)

    def is_connected(self):
        return len(self._connections) > 0

    def read(self):
        if not self._rx_buffer:
            return None
        data = bytes(self._rx_buffer)
        self._rx_buffer = bytearray()
        return data

    def send(self, data):
        if isinstance(data, str):
            data = data.encode()
        for conn_handle in list(self._connections):
            try:
                self._ble.gatts_notify(conn_handle, self._tx_handle, data)
                print("[BLE] Notified", conn_handle, "->", data)
            except Exception as e:
                print("[BLE] Error notify:", e)

    def _advertise(self, name="PROTORP"):
        adv_payload = bytearray(b'\x02\x01\x06') + bytearray((len(name)+1, 0x09)) + name.encode()
        try:
            self._ble.gap_advertise(100, adv_payload)
            print("[BLE] Advertising:", name)
        except Exception as e:
            print("[BLE] Error advertise:", e)

