# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_htu21df import htu21df


i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
htu = htu21df.HTU21DF(i2c)

while True:
    print(f"Temperature: {htu.temperature:.2f}°C")
    print(f"Humidity: {htu.humidity:.2%}%")
    print("")
    time.sleep(1)
