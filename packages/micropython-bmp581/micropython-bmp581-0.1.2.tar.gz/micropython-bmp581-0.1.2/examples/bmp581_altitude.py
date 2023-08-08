# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

from machine import Pin, I2C
from micropython_bmp581 import bmp581

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
bmp = bmp581.BMP581(i2c)

# Oddly first pressure measure after power-on return wrong value.
# so we "burn" one measure
_ = bmp.pressure

print(f"Pressure: {bmp.pressure:.2f}kPa")
print(f"Current altitude: {bmp.altitude:.1f}mts")
