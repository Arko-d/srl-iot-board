from gas import GAS
import utime

multi = GAS(0, 1)

while True: 
    print("NO2 = ", multi.measure_NO2(),end=",")
    print("C2H5OH = ", multi.measure_C2H5OH(),end=",")
    print("VOC = ", multi.measure_VOC(),end=",")
    print("CO = ", multi.measure_CO())
    utime.sleep_ms(1000)

