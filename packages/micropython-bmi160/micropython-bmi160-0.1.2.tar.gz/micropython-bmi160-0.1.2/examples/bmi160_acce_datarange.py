# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_bmi160 import bmi160

i2c = I2C(1, sda=Pin(2), scl=Pin(3))  # Correct I2C pins for RP2040
bmi = bmi160.BMI160(i2c)

bmi.acceleration_range = bmi160.ACCEL_RANGE_4G

while True:
    for data_range in bmi160.acc_range_values:
        print("Current Acceleration Data Rate: ", bmi.acceleration_range)
        for _ in range(10):
            accx, accy, accz = bmi.acceleration
            print(f"x:{accx:.2f}m/s2, y:{accy:.2f}m/s2, z{accz:.2f}m/s2")
            time.sleep(0.5)
        bmi.acceleration_range = data_range
