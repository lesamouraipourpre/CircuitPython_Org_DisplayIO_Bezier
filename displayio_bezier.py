# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 James Carr
#
# SPDX-License-Identifier: MIT
"""
`displayio_bezier`
==================

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

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/lesamouraipourpre/CircuitPython_Org_DisplayIO_Bezier.git"


from math import sqrt
from typing import Tuple
import displayio


MAX_POINTS = 4

PASCALS_TRIANGLE = (
    (1,),
    (1, 1),
    (1, 2, 1),
    (1, 3, 3, 1),
    # We only need the first 4 rows for now
    # (1, 4, 6, 4, 1),
)


class Bezier(displayio.TileGrid):
    # pylint: disable=too-few-public-methods
    """
    Document Bezier
    """

    def __init__(
        self,
        points: Tuple[Tuple[int, int], ...],
        *,
        stroke: float = 1,
        color: int = 0x808080
    ):
        """
        :param points: A tuple of points
        :param float stroke: the width of the Bezier curve, minimum 1. (default is 1)
        :param int color: the color to draw the Bezier curve. (default is Mid Grey (0x808080))
        """
        if len(points) < 2:
            raise ValueError("There must be at least 2 points")
        if len(points) > MAX_POINTS:
            raise ValueError("There must be at most {} points".format(MAX_POINTS))
        if stroke is None or stroke < 1:
            raise ValueError("Stroke must be greater or equal to 1")

        min_x = 1_000_000
        max_x = 0
        min_y = 1_000_000
        max_y = 0
        for x, y in points:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        x = min_x
        y = min_y
        width = max_x - min_x + 1
        height = max_y - min_y + 1

        self._palette = displayio.Palette(2)
        self._palette.make_transparent(0)
        self._palette[1] = color

        # print("Bitmap", width, "x", height)
        self._bitmap = displayio.Bitmap(width, height, 2)
        self._draw_bezier(points, stroke)

        super().__init__(self._bitmap, x=x, y=y, pixel_shader=self._palette)

    def _draw_bezier(self, points, stroke):
        # pylint: disable=too-many-locals
        # pylint: disable=unused-argument  # stroke

        num_steps = 100
        num_points = len(points)
        num_lines = num_points - 1
        x_off, y_off = points[0]
        for i in range(num_lines):
            _x0, _y0 = points[i]
            _x1, _y1 = points[i + 1]
            x_off = min(x_off, _x1)
            y_off = min(y_off, _y1)
            _w = _x1 - _x0
            _h = _y1 - _y0
            num_steps = max(num_steps, _w * _w + _h * _h)
        num_steps = int(sqrt(num_steps) * 2)

        step = 1.0 / num_steps
        _x0, _y0 = points[0]

        _t = 0.0
        while _t <= 1.0:
            _xx = -x_off
            _yy = -y_off
            for i in range(num_points):
                bernstein = (
                    PASCALS_TRIANGLE[num_lines][i]
                    * pow(_t, i)
                    * pow((1 - _t), (num_lines - i))
                )
                x, y = points[i]
                _xx += x * bernstein
                _yy += y * bernstein

            # print(t, int(xx), int(yy))
            self._bitmap[int(_xx), int(_yy)] = 1
            _t += step
