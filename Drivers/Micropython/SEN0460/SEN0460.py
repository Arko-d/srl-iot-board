import machine
import time

class SEN0460:
    # Define constants for selecting different particle measurement types
    PARTICLE_PM1_0_STANDARD   = 0x05
    PARTICLE_PM2_5_STANDARD   = 0x07
    PARTICLE_PM10_STANDARD    = 0x09
    PARTICLE_PM1_0_ATMOSPHERE = 0x0B
    PARTICLE_PM2_5_ATMOSPHERE = 0x0D
    PARTICLE_PM10_ATMOSPHERE  = 0x0F
    PARTICLENUM_0_3_UM_EVERY0_1L_AIR = 0x11
    PARTICLENUM_0_5_UM_EVERY0_1L_AIR = 0x13
    PARTICLENUM_1_0_UM_EVERY0_1L_AIR = 0x15
    PARTICLENUM_2_5_UM_EVERY0_1L_AIR = 0x17
    PARTICLENUM_5_0_UM_EVERY0_1L_AIR = 0x19
    PARTICLENUM_10_UM_EVERY0_1L_AIR  = 0x1B
    PARTICLENUM_GAIN_VERSION = 0x1D

    def _init_(self, i2c, addr):
        # Initialize the sensor with the I2C interface and its address
        self.i2c = i2c
        self.addr = addr

    def gain_particle_concentration_ugm3(self, PMtype):
        # Get the particle concentration in µg/m³ for a specified PM type
        buf = self.read_reg(PMtype, 2)
        concentration = (buf[0] << 8) + buf[1]  # Combine two bytes to form the concentration value
        return concentration

    def gain_particlenum_every0_1l(self, PMtype):
        # Get the particle count for a specified PM type in every 0.1L of air
        buf = self.read_reg(PMtype, 2)
        particlenum = (buf[0] << 8) + buf[1]  # Combine two bytes to form the particle count
        return particlenum

    def gain_version(self):
        # Get the sensor's firmware version
        version = self.read_reg(self.PARTICLENUM_GAIN_VERSION, 1)
        return int(version[0])

    def set_lowpower(self):
        # Set the sensor to low power mode
        mode = bytearray([0x01])
        self.write_reg(0x01, mode)

    def awake(self):
        # Wake up the sensor from low power mode
        mode = bytearray([0x02])
        self.write_reg(0x01, mode)

    def write_reg(self, reg, data):
        # Write data to a specific register on the sensor
        while True:
            try:
                self.i2c.writeto(self.addr, bytearray([reg]) + data)  # Combine register and data and write to I2C
                return
            except:
                print("please check connect!")  # Retry if there's a connection issue
                time.sleep(1)
                return

    def read_reg(self, reg, len):
        # Read a specified number of bytes from a register
        try:
            rslt = self.i2c.readfrom(self.addr, len)  # Read the required length of data
            return rslt
        except:
            return -1  # Return -1 if there's an error


# Create an I2C object with SCL (clock) on GPIO 12 and SDA (data) on GPIO 11
i2c = machine.SoftI2C(scl=machine.Pin(12), sda=machine.Pin(11))

# Create an instance of the air quality sensor with the I2C address (e.g., 0x19)
sensor = SEN0460(i2c, 0x19)  # Replace 0x19 with your sensor's I2C address

def main():
    while True:
        # Get and print the sensor's firmware version
        version = sensor.gain_version()
        print("Sensor version:", version)
        
        # Wake up the sensor
        sensor.awake()
        time.sleep(1)  # Allow some time for the sensor to wake up

        # Get and print particle concentrations in µg/m³ for standard PM1.0, PM2.5, and PM10
        pm1_0_std = sensor.gain_particle_concentration_ugm3(SEN0460.PARTICLE_PM1_0_STANDARD)
        pm2_5_std = sensor.gain_particle_concentration_ugm3(SEN0460.PARTICLE_PM2_5_STANDARD)
        pm10_std = sensor.gain_particle_concentration_ugm3(SEN0460.PARTICLE_PM10_STANDARD)

        print("PM1.0 (Standard):", pm1_0_std, "µg/m³")
        print("PM2.5 (Standard):", pm2_5_std, "µg/m³")
        print("PM10 (Standard):", pm10_std, "µg/m³")

        # Get and print particle concentrations in µg/m³ for atmospheric PM1.0, PM2.5, and PM10
        pm1_0_atmos = sensor.gain_particle_concentration_ugm3(SEN0460.PARTICLE_PM1_0_ATMOSPHERE)
        pm2_5_atmos = sensor.gain_particle_concentration_ugm3(SEN0460.PARTICLE_PM2_5_ATMOSPHERE)
        pm10_atmos = sensor.gain_particle_concentration_ugm3(SEN0460.PARTICLE_PM10_ATMOSPHERE)

        print("PM1.0 (Atmosphere):", pm1_0_atmos, "µg/m³")
        print("PM2.5 (Atmosphere):", pm2_5_atmos, "µg/m³")
        print("PM10 (Atmosphere):", pm10_atmos, "µg/m³")

        # Get and print the particle count for different particle sizes in every 0.1L of air
        num_0_3_um = sensor.gain_particlenum_every0_1l(SEN0460.PARTICLENUM_0_3_UM_EVERY0_1L_AIR)
        num_0_5_um = sensor.gain_particlenum_every0_1l(SEN0460.PARTICLENUM_0_5_UM_EVERY0_1L_AIR)
        num_1_0_um = sensor.gain_particlenum_every0_1l(SEN0460.PARTICLENUM_1_0_UM_EVERY0_1L_AIR)
        num_2_5_um = sensor.gain_particlenum_every0_1l(SEN0460.PARTICLENUM_2_5_UM_EVERY0_1L_AIR)
        num_5_0_um = sensor.gain_particlenum_every0_1l(SEN0460.PARTICLENUM_5_0_UM_EVERY0_1L_AIR)
        num_10_um = sensor.gain_particlenum_every0_1l(SEN0460.PARTICLENUM_10_UM_EVERY0_1L_AIR)

        print("Particles 0.3µm:", num_0_3_um, "per 0.1L air")
        print("Particles 0.5µm:", num_0_5_um, "per 0.1L air")
        print("Particles 1.0µm:", num_1_0_um, "per 0.1L air")
        print("Particles 2.5µm:", num_2_5_um, "per 0.1L air")
        print("Particles 5.0µm:", num_5_0_um, "per 0.1L air")
        print("Particles 10µm:", num_10_um, "per 0.1L air")

        # Set the sensor back to low power mode
        sensor.set_lowpower()
        print("----------------------------------------------------\n")
        time.sleep(3)  # Wait before repeating the loop

if _name_ == "_main_":
    main()