# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 James Carr
#
# SPDX-License-Identifier: Unlicense

import time
import board
import displayio

from displayio_bezier import Bezier

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

# bezier = Bezier(points=((0, 0), (display.width, display.height)))
# bezier = Bezier(points=((0, 0), (0, display.height), (display.width, display.height)))
# bezier = Bezier(
#     points=(
#         (0, 0),
#         (0, display.height),
#         (display.width, display.height),
#         (display.width, 0),
#     ),
#     color=0xFFFFFF
# )
# main_group.append(bezier)

R = 0xFF0000
G = 0x00FF00
B = 0x0000FF

### C ###
main_group.append(Bezier(points=((120, 80), (110, 30), (80, 30)), color=R))
main_group.append(Bezier(points=((80, 30), (30, 30), (30, 120)), color=G))
main_group.append(Bezier(points=((30, 120), (30, 210), (80, 210)), color=B))
main_group.append(Bezier(points=((80, 210), (110, 210), (120, 160)), color=R))

### P ###
main_group.append(Bezier(points=((190, 210), (190, 30)), color=G))
main_group.append(Bezier(points=((190, 30), (240, 30)), color=B))
main_group.append(Bezier(points=((240, 30), (290, 30), (290, 90)), color=R))
main_group.append(Bezier(points=((290, 90), (290, 150), (240, 150)), color=G))
main_group.append(Bezier(points=((240, 150), (190, 150)), color=B))

display.show(main_group)

while True:
    time.sleep(1)
