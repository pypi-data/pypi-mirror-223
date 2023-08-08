# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_pct2075 import pct2075

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
pct = pct2075.PCT2075(i2c)

pct.high_temperature_threshold = 29
pct.temperature_hysteresis = 27.0
pct.high_temp_active_high = False

while True:
    print(f"Temperature {pct.temperature:.2f}°C")
    print()
    time.sleep(0.5)
