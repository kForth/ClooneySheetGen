from reportlab.lib.colors import Color

import draw_functions as draw
from fields._base import FieldBase


class Markers(FieldBase):
    def draw(self, canvas, _, __, config):
        super().__init__()
        marker_color = Color(*config["marker_colour"], alpha=1.0)
        draw.box(canvas,
                 0,
                 0,
                 config["marker_size"], stroke=0, fill=1, fill_color=marker_color)
        draw.box(canvas,
                 self.SHEET_WIDTH - config["marker_size"],
                 0,
                 config["marker_size"], stroke=0, fill=1, fill_color=marker_color)
        draw.box(canvas,
                 0,
                 self.SHEET_HEIGHT - config["marker_size"],
                 config["marker_size"], stroke=0, fill=1, fill_color=marker_color)
        draw.box(canvas,
                 self.SHEET_WIDTH - config["marker_size"],
                 self.SHEET_HEIGHT - config["marker_size"],
                 config["marker_size"], stroke=0, fill=1, fill_color=marker_color)
        draw.rectangle(canvas, config["marker_size"], config["marker_size"],
                       self.SHEET_WIDTH - config["marker_size"] * 2,
                       self.SHEET_HEIGHT - config["marker_size"] * 2)
