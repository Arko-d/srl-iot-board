from machine import I2C,Pin
from ssd1306 import SSD1306_I2C
import utime
import math
i2c = I2C(id=0, scl=Pin(1), sda=Pin(0), freq=400000)
screen = SSD1306_I2C(128,32,i2c)
x=0
y=0
dx="right"
dy="down"
while True:
    if dx=="right":
        x=(x+1)
        if x==100:
            dx="left"
    if dx=="left":
        x=(x-1)
        if x==0:
            dx="right"
    screen.fill(0)
    if dy=="up":
        y=y-1
        if y==0:
            dy="down"
    if dy=="down":
        y=y+1
        if y==20:
            dy="up"
    screen.text('Arko', x,y)
    screen.show()
    utime.sleep_ms(100)


