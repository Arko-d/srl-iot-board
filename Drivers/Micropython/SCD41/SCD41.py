# scd4x.py

import machine
import time

class SCD4X:
    DEFAULT_ADDRESS = 0x62
    START_PERIODIC_MEASUREMENT = 0x21B1
    READ_MEASUREMENT = 0xEC05
    STOP_PERIODIC_MEASUREMENT = 0x3F86
    DATA_READY = 0xE4B8

    def __init__(self, i2c_bus, address=DEFAULT_ADDRESS):
        self.i2c = i2c_bus
        self.address = address

    def _send_command(self, cmd):
        cmd_bytes = bytes([(cmd >> 8) & 0xFF, cmd & 0xFF])
        self.i2c.writeto(self.address, cmd_bytes)
        time.sleep(0.05)  # Allow time for the command to be processed

    def start_measurement(self):
        """Start periodic measurements."""
        self._send_command(self.START_PERIODIC_MEASUREMENT)

    def stop_measurement(self):
        """Stop periodic measurements."""
        self._send_command(self.STOP_PERIODIC_MEASUREMENT)

    def read_measurement(self):
        """Read measurement data from the sensor."""
        self._send_command(self.READ_MEASUREMENT)
        time.sleep(0.1)  # Allow time for the data to be available
        try:
            data = self.i2c.readfrom(self.address, 18)
            co2 = (data[0] << 8) | data[1]
            temp = (data[3] << 8) | data[4]
            humidity = (data[6] << 8) | data[7]
            temperature = -45 + 175 * (temp / 2 ** 16)
            relative_humidity = 100 * (humidity / 2 ** 16)
            return co2, temperature, relative_humidity
        except OSError as e:
            print("Read error:", e)
            return 0, 0, 0

    def is_data_ready(self):
        """Check if the data is ready to be read."""
        self._send_command(self.DATA_READY)
        time.sleep(0.1)
        try:
            response = self.i2c.readfrom(self.address, 3)
            return not ((response[0] & 0x03 == 0) and (response[1] == 0))
        except OSError as e:
            print("Data ready check error:", e)
            return False
