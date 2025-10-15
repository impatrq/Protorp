from machine import Pin
import time

class Tx:
    def __init__(self, pin):  
        self.pin = Pin(pin, Pin.OUT)
        self.pin.value(0)

    def send_byte(self, byte):
        for i in range(8):
            bit = (byte >> (7 - i)) & 1
            self.pin.value(bit)
            time.sleep_us(500)
        self.pin.value(0)

class Rx:
    def __init__(self, pin):  
        self.pin = Pin(pin, Pin.IN)

    def listen(self):
        byte = 0
        for i in range(8):
            bit = self.pin.value()
            byte = (byte << 1) | bit
            time.sleep_us(500)
        return byte
