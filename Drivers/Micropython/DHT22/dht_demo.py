from machine import Pin
import dht
import utime

dht_sensor = dht.DHT22(Pin(4))
while True:
    dht_sensor.measure()
    temperature = float(dht_sensor.temperature())
    humidity = float(dht_sensor.humidity())
    print("Temperature= ",temperature)
    print("Humidity= ",humidity)
    utime.sleep_ms(3000)


