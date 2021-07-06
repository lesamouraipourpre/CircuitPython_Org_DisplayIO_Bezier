# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 James Carr
#
# SPDX-License-Identifier: Unlicense

import time
import board
import displayio

from displayio_bezier.bezier import Bezier
from displayio_bezier.path import BezierPath

# Create a display object

if hasattr(board, "DISPLAY"):
    display = board.DISPLAY
else:
    # What should I do here?
    raise NotImplementedError("Provide a Display")

print("Display size: {}x{}".format(display.width, display.height))
main_group = displayio.Group()

# Make a background color fill
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
main_group.append(bg_sprite)

### C ###
c_path = BezierPath((120, 80))
c_path.cubic_to((80, 30), handle=(110, 30))
c_path.cubic_to((30, 120), handle=(30, 30))
c_path.cubic_to((80, 210), handle=(30, 210))
c_path.cubic_to((120, 160), handle=(110, 210))
main_group.append(Bezier(c_path, color=0xFF8000, stroke=2))

### P ###
p_path = BezierPath((190, 210))
p_path.line_to((190, 30))
p_path.line_to((240, 30))
p_path.cubic_to((290, 90), handle=(290, 30))
p_path.cubic_to((240, 150), handle=(290, 150))
p_path.line_to((190, 150))
main_group.append(Bezier(p_path, color=0x0080FF, stroke=4))

display.show(main_group)

while True:
    time.sleep(1)
