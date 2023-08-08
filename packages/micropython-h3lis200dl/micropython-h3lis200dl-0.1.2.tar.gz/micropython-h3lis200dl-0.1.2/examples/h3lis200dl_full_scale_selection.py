# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_h3lis200dl import h3lis200dl

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
h3lis = h3lis200dl.H3LIS200DL(i2c)

h3lis.full_scale_selection = h3lis200dl.SCALE_100G

while True:
    for full_scale_selection in h3lis200dl.full_scale_selection_values:
        print("Current Full scale selection setting: ", h3lis.full_scale_selection)
        for _ in range(10):
            accx, accy, accz = h3lis.acceleration
            print(f"x:{accx:2f}g, y:{accy:2f}g, z:{accz:2f}g")
            time.sleep(0.5)
        h3lis.full_scale_selection = full_scale_selection
