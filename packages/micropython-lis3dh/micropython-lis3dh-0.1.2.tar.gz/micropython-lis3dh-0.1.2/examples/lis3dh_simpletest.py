# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya

import time
from machine import Pin, I2C
from micropython_lis3dh import lis3dh

i2c = I2C(sda=Pin(8), scl=Pin(9))  # Correct I2C pins for UM FeatherS2
lis = lis3dh.LIS3DH(i2c)

for _ in range(10):
    accx, accy, accz = lis.acceleration
    print(f"x: {accx}m/s^2, y: {accy}m/s^2, z: {accz}m/s^2")
    print()
    time.sleep(1)
