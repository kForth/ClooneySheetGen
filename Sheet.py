from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from Fields import *

class Sheet:
    def __init__(self, config):
        self.fields = []
        self.config = config
        self.canvas = canvas.Canvas(config["filename"] + ".pdf", pagesize = letter)
        self.headers = []

    def add_field(self, field):
        if field.get_label() != "=":
            self.headers.append(field.get_label())
        self.fields.append(field)

    def draw_sheet(self, match, pos):

        with open("StrongholdFields.csv", "w") as f:
            f.write("")
            f.close()

        y_pos = self.config["marker_size"] + 1.125
        Markers().draw(self.canvas, self.config)
        y_pos += Header(match, pos).draw(self.canvas, self.config["x_pos"] + self.config["marker_size"], y_pos, self.config)
        horizontal_accum = 0

        for f_num in range(len(self.fields)):
            f = self.fields[f_num]
            try:
                f_next = self.fields[f_num + 1]
            except:
                f_next = Divider()

            if f.get_type() == "Boolean" and horizontal_accum < 2:
                if f_num < (len(self.fields) - 1) and self.fields[f_num + 1].get_type() == "Boolean":
                    f.draw(self.canvas, self.config["x_pos"] + self.config["marker_size"] + (self.config["bool_x_offset"] * horizontal_accum), y_pos, self.config)
                    horizontal_accum += 1
                else:
                    y_pos += f.draw(self.canvas, self.config["x_pos"] + self.config["marker_size"] + (self.config["bool_x_offset"] * horizontal_accum), y_pos, self.config)
                    horizontal_accum = 0
            else:
                y_pos += f.draw(self.canvas, self.config["x_pos"] + self.config["marker_size"] + (self.config["bool_x_offset"] * horizontal_accum), y_pos, self.config)
                horizontal_accum = 0

        return

    def draw_sheets(self):
        for p in range(0, 6):
            for m in range(1, self.config["num_sheets"]+1):
                self.draw_sheet(m, p)
                self.canvas.showPage()
            if self.config["spacer_page"]:
                self.canvas.showPage()
        self.canvas.save()
        open(self.config["filename"] + "Fields.csv", "a").write(','.join(self.headers))
