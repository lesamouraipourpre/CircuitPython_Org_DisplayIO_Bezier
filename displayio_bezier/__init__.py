# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 James Carr
#
# SPDX-License-Identifier: MIT

"""
displayio_bezier
================

Draw Bezier curves with DisplayIO

* Author(s): James Carr

Implementation Notes
--------------------

**Hardware:**

* Any display capable of being used with DisplayIO

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

MAX_POINTS = 5

PASCALS_TRIANGLE = (
    (1,),  # point
    (1, 1),  # line to
    (1, 2, 1),  # cubic to
    (1, 3, 3, 1),  # quartic to
    (1, 4, 6, 4, 1),  # quintic to
    # We only need the first 5 rows for now
    # (1, 5, 10, 10, 5, 1),
    # (1, 6, 15, 20, 15, 6, 1),
    # (1, 7, 21, 35, 35, 21, 7, 1),
    # (1, 8, 28, 56, 70, 56, 28, 8, 1),
    # (1, 9, 36, 84, 126, 126, 84, 36, 9, 1),
)
