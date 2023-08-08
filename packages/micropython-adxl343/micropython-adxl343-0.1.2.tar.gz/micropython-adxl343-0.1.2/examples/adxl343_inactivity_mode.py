# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_adxl343 import adxl343

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
adx = adxl343.ADXL343(i2c)

adx.inactivity_mode = adxl343.INACTIVITY_ENABLED

while True:
    for inactivity_mode in adxl343.inactivity_mode_values:
        print("Current Inactivity mode setting: ", adx.inactivity_mode)
        for _ in range(10):
            accx, accy, accz = adx.acceleration
            print(f"x:{accx:.2f}m/s2, y:{accy:.2f}m/s2, z:{accz:.2f}m/s2")
            time.sleep(0.5)
