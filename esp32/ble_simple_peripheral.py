import bluetooth
from ble_advertising import advertising_payload
from micropython import const

_FLAG_READ = const(0x0002)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

class BLESimplePeripheral:
    def __init__(self, ble, name="PROTORP"):
        self._ble = ble
        self._ble.active(True)
        self._ble.config(gap_name=name)
        self._ble.irq(self._irq)
        self._connections = set()
        self._write_callback = None

        
        self._service_uuid = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
        self._rx_uuid = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")  
        self._tx_uuid = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")  

        self._rx = (self._rx_uuid, _FLAG_WRITE)
        self._tx = (self._tx_uuid, _FLAG_NOTIFY | _FLAG_READ)
        self._service = (self._service_uuid, (self._rx, self._tx))
        ((self._rx_handle, self._tx_handle),) = self._ble.gatts_register_services((self._service,))

        self._payload = advertising_payload(name=name, services=[self._service_uuid])
        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            if value_handle == self._rx_handle and self._write_callback:
                value = self._ble.gatts_read(self._rx_handle)
                self._write_callback(value)

    def on_write(self, callback):
        self._write_callback = callback

    def send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._tx_handle, data)

    def _advertise(self, interval_us=100000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)
