import machine
import time
import sys
from machine import Pin, UART

# Setup UART
ser = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))  
ser.init(115200, bits=8, parity=None, stop=1)

phone_number = '+919831534925'  
text_message = 'Your A/C Credited INR 5,000.00 on 24/08/24 -Deposit by transfer from IISc Bangalore.'
rec_buff = ''

def send_at(command, back, timeout):
    rec_buff = b''
    ser.write((command + '\r\n').encode())
    time.sleep(timeout)
    if ser.any():
        time.sleep(0.01)
        rec_buff = ser.read()
    if back not in rec_buff.decode():
        print(command + ' ERROR')
        print(command + ' back:\t' + rec_buff.decode())
        return 0
    else:
        print(rec_buff.decode())
        return 1

def SendShortMessage(phone_number, text_message):
    print("Setting SMS mode...")
    send_at('AT+COPS?', 'OK', 3)
    send_at('AT+CSQ', 'OK', 3)
    send_at("AT+CMGF=1", "OK", 1)
    print("Sending Short Message")
    answer = send_at("AT+CMGS=\"" + phone_number + "\"", ">", 2)
    if 1 == answer:
        ser.write(text_message.encode())
        ser.write(b'\x1A')
        answer = send_at('', 'OK', 20)
        if 1 == answer:
            print('send successfully')
        else:
            print('error')
    else:
        print('error%d' % answer)

def ReceiveShortMessage():
    rec_buff = ''
    print('Setting SMS mode...')
    send_at('AT+COPS?', 'OK', 3)
    send_at('AT+CSQ', 'OK', 3)
    send_at('AT+CMGF=1', 'OK', 1)
    send_at('AT+CPMS=\"SM\",\"SM\",\"SM\"', 'OK', 1)
    answer = send_at('AT+CMGR=1', '+CMGR:', 2)
    if 1 == answer:
        answer = 0
        if 'OK' in rec_buff:
            answer = 1
            print(rec_buff)
    else:
        print('error%d' % answer)
        return False
    return True

try:
    print('Sending Short Message Test:')
    SendShortMessage(phone_number, text_message)
    print('Receive Short Message Test:\n')
    print('Please send message to phone ' + phone_number)
    ReceiveShortMessage()
except Exception as e:
    print('Error:', e)
    if ser is not None:
        ser.deinit()
