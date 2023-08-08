# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
import adt7410

i2c = board.I2C()  # uses board.SCL and board.SDA
adt = adt7410.ADT7410(i2c)

while True:
    print(f"Temperature: {adt.temperature:.2f}°C")
    print()
    time.sleep(0.5)
