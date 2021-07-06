# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 James Carr
#
# SPDX-License-Identifier: MIT

"""
displayio_bezier.path
=====================
"""

try:
    from typing import Tuple

    XYPos = Tuple[int, int]
    Positions = Tuple[XYPos, ...]
    Segment = Tuple[XYPos, Positions]
    Bounds = Tuple[int, int, int, int]
except ImportError:
    pass

import displayio

from . import PASCALS_TRIANGLE


class BezierPath:
    """
    Document BezierPath
    """

    def __init__(self, start_position: XYPos):
        self._start_pos = start_position
        self._current_pos = start_position
        self._segments = []
        self._closed = False
        self._bounds = None

    def line_to(self, position: XYPos):
        """
        Document me - line_to
        """
        self.bezier_to(position, tuple())

    def cubic_to(self, position: XYPos, handle: XYPos):
        """
        Document me - cubic_to
        """
        self.bezier_to(position, (handle,))

    def quartic_to(self, position: XYPos, handle1: XYPos, handle2: XYPos):
        """
        Document me - quartic_to
        """
        self.bezier_to(position, (handle1, handle2))

    def quintic_to(
        self, position: XYPos, handle1: XYPos, handle2: XYPos, handle3: XYPos
    ):
        """
        Document me - quintic_to
        """
        self.bezier_to(position, (handle1, handle2, handle3))

    def close_path(self):
        """
        Document me - close_path
        """
        if not self._closed and self._current_pos != self._start_pos:
            self.line_to(self._start_pos)
        self._closed = True

    def bezier_to(self, position: XYPos, handles: Positions):
        """
        Document me - bezier_to
        """
        if self._closed:
            raise ValueError("The Path is already closed.")
        self._segments.append((position, handles))
        self._current_pos = position
        self._bounds = None

    @property
    def start_position(self) -> XYPos:
        """
        The starting position of the path.

        :return: XYPos
        """
        return self._start_pos

    @property
    def bounds(self) -> Bounds:
        """
        The bounds of the control points of the path. The bounds of the path
        itself may be noticeably smaller.

        :return: Bounds
        """
        if self._bounds is not None:
            return self._bounds

        min_x, min_y = self._start_pos
        max_x, max_y = min_x, min_y

        for end_pos, handles in self._segments:
            x, y = end_pos
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            for x, y in handles:
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

        x, y = min_x, min_y
        width = max_x - min_x + 1
        height = max_y - min_y + 1

        self._bounds = (x, y, width, height)
        return self._bounds

    def draw_to_bitmap(self, bitmap: displayio.Bitmap, origin: XYPos = (0, 0)):
        """
        :param displayio.Bitmap bitmap: The bitmap
        :param XYPos origin: The offset of the (0,0) position of the bitmap.
            This will usually be the (x,y) position of the bitmap in it's
            containing Group.
        """

        start_pos = self._start_pos
        for end_pos, handles in self._segments:
            self._draw_segment(bitmap, origin, start_pos, end_pos, handles)
            start_pos = end_pos

    def _draw_segment(
        self,
        bitmap: displayio.Bitmap,
        origin: XYPos,
        start_pos: XYPos,
        end_pos: XYPos,
        handles: Positions,
    ):
        # pylint: disable=too-many-arguments,too-many-locals,no-self-use

        positions = list()
        positions.append(start_pos)
        for handle in handles:
            positions.append(handle)
        positions.append(end_pos)

        num_steps = 250
        num_points = len(positions)
        num_lines = num_points - 1
        x_off, y_off = origin

        step = 1.0 / num_steps
        _x0, _y0 = positions[0]
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
                x, y = positions[i]
                _xx += x * bernstein
                _yy += y * bernstein
            bitmap[int(_xx), int(_yy)] = 1
            _t += step

    #     num_steps = 100
    #     for i in range(num_lines):
    #         _x0, _y0 = points[i]
    #         _x1, _y1 = points[i + 1]
    #         x_off = min(x_off, _x1)
    #         y_off = min(y_off, _y1)
    #         _w = _x1 - _x0
    #         _h = _y1 - _y0
    #         num_steps = max(num_steps, _w * _w + _h * _h)
    #     num_steps = int(sqrt(num_steps) * 2)
