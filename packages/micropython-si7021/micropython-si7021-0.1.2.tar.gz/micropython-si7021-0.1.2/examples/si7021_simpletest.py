# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya

import time
from machine import Pin, I2C
from micropython_si7021 import si7021

i2c = I2C(sda=Pin(8), scl=Pin(9))  # Correct I2C pins for UM FeatherS2
si = si7021.SI7021(i2c)

while True:
    print(f"Temperature: {si.temperature:.2f}")
    print(f"Humidity: {si.humidity:.2%}")
    print()
    time.sleep(1)
