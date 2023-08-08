# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_adt7410 import adt7410

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
adt = adt7410.ADT7410(i2c)

while True:
    print(f"Temperature: {adt.temperature:.2f}°C")
    print()
    time.sleep(0.5)
