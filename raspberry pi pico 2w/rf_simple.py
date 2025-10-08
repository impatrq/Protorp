from machine import Pin
import time

class Tx:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)

    def send_byte(self, value):
        bin_str = bin(value)[2:]
        while len(bin_str) < 8:
            bin_str = '0' + bin_str
        bits = [int(b) for b in bin_str]
        header = [1, 1, 1, 1, 1, 1, 1, 1]
        self._send_bits(header + bits)

    def _send_bits(self, bits):
        for bit in bits:
            self.pin.value(bit)
            time.sleep_us(500)
            self.pin.value(0)
            time.sleep_us(500)

class Rx:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)

    def listen(self):
        while self.pin.value() == 0:
            pass
        bits = []
        for _ in range(16):  # 8 header + 8 datos
            time.sleep_us(500)
            bits.append(self.pin.value())
            time.sleep_us(500)
        data_bits = bits[8:]
        value = 0
        for bit in data_bits:
            value = (value << 1) | bit
        return value