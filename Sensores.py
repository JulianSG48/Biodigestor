# filename: main.py
# platform: micropython-esp32
# send: wifi
# ip_mpy: 192.168.4.1
# serialport: 

from machine import Pin, SoftI2C, ADC
from machine_i2c_lcd import I2cLcd
from time import sleep
import onewire, ds18x20

I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS = 0x27, 2, 16
i2c = SoftI2C(sda=Pin(21), scl=Pin(22), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

ds_sensor = ds18x20.DS18X20(onewire.OneWire(Pin(4)))
roms = ds_sensor.scan()
adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)

V_SUPPLY, P_MAX, V_MIN, V_MAX = 3.3, 400, 0.5, 4.5
lcd.custom_char(0, bytearray([0x04, 0x0A, 0x0A, 0x0A, 0x0A, 0x1B, 0x1F, 0x0E]))
lcd.custom_char(1, bytearray([0x0E, 0x11, 0x11, 0x0E, 0x04, 0x04, 0x1F, 0x04]))

try:
    while True:
        ds_sensor.convert_temp()
        sleep(0.75)
        temp = ds_sensor.read_temp(roms[0]) if roms else 0.0
        pressure = max(0, min(P_MAX, ((adc.read() / 4095.0) * V_SUPPLY - V_MIN) / (V_MAX - V_MIN) * P_MAX))

        lcd.clear()
        lcd.putstr("Temperatura:")
        lcd.putchar(chr(0))
        lcd.putstr(" {:.1f}C".format(temp))
        lcd.move_to(0, 1)
        lcd.putstr("Presion:")
        lcd.putchar(chr(1))
        lcd.putstr(" {:.1f} kPa".format(pressure))
        sleep(2)
except KeyboardInterrupt:
    lcd.backlight_off()
    lcd.display_off()