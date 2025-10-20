import bluetooth
import struct
import time
from micropython import const


_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX   = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
              bluetooth.FLAG_NOTIFY,)
_UART_RX   = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
              bluetooth.FLAG_WRITE,)
_UART_SERVICE = (_UART_UUID, (_UART_TX, _UART_RX,),)

class BLESimplePeripheral:
    def __init__(self, ble, name="PROTORP"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._connections = set()
        self._rx_buffer = bytearray()
        self._advertise(name)

    def _irq(self, event, data):
        if event == 1:  
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == 2:  
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            self._advertise()
        elif event == 3:  
            conn_handle, value_handle = data
            self._rx_buffer += self._ble.gatts_read(value_handle)

    def is_connected(self):
        return len(self._connections) > 0

    def read(self):
        if not self._rx_buffer:
            return None
        data = self._rx_buffer
        self._rx_buffer = bytearray()
        return data

    def send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._tx_handle, data)

    def _advertise(self, name="PROTORP"):
        adv_data = bytearray("\x02\x01\x06" + chr(len(name)+1) + "\x09" + name, "utf-8")
        self._ble.gap_advertise(100, adv_data)
