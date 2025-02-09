#!/bin/env python
from rgbmatrix import graphics
import sys

sys.path.append("../")


class draw:
    def local_train(self, canvas, x, y, color):
        # Draws local train circle
        graphics.DrawLine(canvas, x + 2, y + 0, x + 6, y + 0, color)
        graphics.DrawLine(canvas, x + 1, y + 1, x + 7, y + 1, color)
        graphics.DrawLine(canvas, x + 0, y + 2, x + 8, y + 2, color)
        graphics.DrawLine(canvas, x + 0, y + 3, x + 8, y + 3, color)
        graphics.DrawLine(canvas, x + 0, y + 4, x + 8, y + 4, color)
        graphics.DrawLine(canvas, x + 0, y + 5, x + 8, y + 5, color)
        graphics.DrawLine(canvas, x + 0, y + 6, x + 8, y + 6, color)
        graphics.DrawLine(canvas, x + 1, y + 7, x + 7, y + 7, color)
        graphics.DrawLine(canvas, x + 2, y + 8, x + 6, y + 8, color)

    def express_train(self, canvas, x, y, color):
        # Draw express train diamond
        graphics.DrawLine(canvas, x + 4, y + 0, x + 4, y + 0, color)
        graphics.DrawLine(canvas, x + 3, y + 1, x + 5, y + 1, color)
        graphics.DrawLine(canvas, x + 2, y + 2, x + 6, y + 2, color)
        graphics.DrawLine(canvas, x + 1, y + 3, x + 7, y + 3, color)
        graphics.DrawLine(canvas, x + 0, y + 4, x + 8, y + 4, color)
        graphics.DrawLine(canvas, x + 1, y + 5, x + 7, y + 5, color)
        graphics.DrawLine(canvas, x + 2, y + 6, x + 6, y + 6, color)
        graphics.DrawLine(canvas, x + 3, y + 7, x + 5, y + 7, color)
        graphics.DrawLine(canvas, x + 4, y + 8, x + 4, y + 8, color)
