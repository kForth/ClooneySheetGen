from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from math import ceil

pdfmetrics.registerFont(TTFont("OpenSansEmoji", "OpenSansEmoji.ttf"))

from Fields import *

class Sheet:
    def __init__(self, config):
        self.fields = []
        self.config = config
        self.canvas = canvas.Canvas(config["filename"] + ".pdf", pagesize = letter)
        self.canvas.setFont("OpenSansEmoji", 1)
        self.headers = []

    def add_field(self, field):
        if field.get_label() != "=":
            self.headers.append(field.get_label())
        self.fields.append(field)

    def draw_sheet(self, match, pos):
        with open(self.config["filename"] + "Fields.csv", "w") as f:
            f.write("")
            f.close()

        y_pos = self.config["marker_size"] + 1.125
        Markers().draw(self.canvas, self.config)
        y_pos += Header(match, pos).draw(self.canvas, self.config["x_pos"] + self.config["marker_size"], y_pos, self.config)
        horizontal_accum = 0
        line_width = 0
        prev_y = 0
        seg_width = (8.5 - self.config["marker_size"] * 2) / 4

        for f_num in range(len(self.fields)):
            x_pos = self.config["x_pos"]

            f = self.fields[f_num]
            f_width = ceil(f.calc_width(self.config) / seg_width)
            t = False
            if f.prev_line and f_width <= 4 - line_width:
                t = True
                if line_width == 0:
                    y_pos += prev_y
                x_pos += (self.config["box_size"] + self.config["box_spacing"]) * self.config["bool_x_offset"] * line_width
                line_width += f_width
            else:
                y_pos += prev_y
                line_width = f_width
            if line_width > 4:
                line_width = 0

            prev_y = f.draw(self.canvas, x_pos + self.config["marker_size"], y_pos, self.config)

    def draw_sheets(self):
        for p in range(0, 6):
            for m in range(1, self.config["num_sheets"]+1):
                self.draw_sheet(m, p)
                self.canvas.showPage()
            if self.config["spacer_page"]:
                self.canvas.showPage()
        self.canvas.save()
        # open(self.config["filename"] + "Fields.csv", "a").write(','.join(self.headers))
