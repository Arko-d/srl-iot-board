import sen0177

dust_sensor = sen0177.SEN0177(0)
while(True):
    dust_sensor.read()
    print("PM 1.0 = ",dust_sensor.data['pm10'])
    print("PM 2.5 = ",dust_sensor.data['pm25'])
    print("PM 10.0 = ",dust_sensor.data['pm100'])

