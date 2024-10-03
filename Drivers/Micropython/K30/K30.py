from machine import I2C, Pin
import time

class K30:
    def __init__(self, i2c, address=0x68):
        self.i2c = i2c
        self.address = address
        self.co2_read_command = bytearray([0x22, 0x00, 0x08, 0x2A])  # Command to read CO2

    def read_co2(self):
        try:
            # Write the CO2 read command to the sensor
            self.i2c.writeto(self.address, self.co2_read_command)
            
            # Wait 38ms for the sensor to process the command and generate a response
            time.sleep_ms(38)
            
            # Read 4 bytes from the sensor
            in_buf = bytearray(4)
            self.i2c.readfrom_into(self.address, in_buf)

            # Calculate the CO2 value from the received data
            co2_value = (in_buf[1] << 8) | in_buf[2]

            # Verify checksum: sum of the first three bytes should equal the fourth byte
            checksum = (in_buf[0] + in_buf[1] + in_buf[2]) & 0xFF  # Keep within byte range
            if checksum != in_buf[3]:
                raise ValueError("Checksum error: expected {}, got {}".format(checksum, in_buf[3]))

            return co2_value

        except OSError as e:
            print("I2C communication error: ", e)
            return -1  # Indicate an error