from math import ceil

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import json

from fields import *

pdfmetrics.registerFont(TTFont("OpenSansEmoji", "resources/OpenSansEmoji.ttf"))

field_types = [Barcode, Boolean, BoxNumber, BulkOptions, Digits, Divider, Header, HorizontalOptions, Image, Markers,
               Numbers, SevenSegment, String]
valid_fields = map(lambda x: x.__name__, field_types)


class Sheet:
    def __init__(self, config):
        self.fields = []
        self.config = config
        self.canvas = canvas.Canvas(config["filename"] + ".pdf", pagesize=letter)
        self.canvas.setFont("OpenSansEmoji", 1)
        self.headers = []
        self.json_fields = {}
        self.first_sheet = True

    def _add_field(self, field):
        if field.get_label() is not None:
            self.headers.append(field.get_label())
        self.fields.append(field)

    def _draw_sheet(self, match, pos):
        self.canvas.setFont("OpenSansEmoji", 1)
        filename = str(self.config["filename"]).lower() + "_fields.json"
        if self.first_sheet:
            with open(filename, "w") as f:
                f.write("")
                f.close()

        y_pos = self.config["marker_size"] + 1.125
        Markers().draw(self.canvas, 0, 0, self.config)
        header = Header(match, pos)
        header_height, scan_info = header.draw(self.canvas, self.config["x_pos"] + self.config["marker_size"], y_pos,
                                               self.config)
        y_pos += header_height

        scan_info = scan_info

        line_width = 0
        prev_y = 0
        seg_width = (8.5 - self.config["marker_size"] * 2) / 4

        for f_num in range(len(self.fields)):
            x_pos = self.config["x_pos"]
            f = self.fields[f_num]
            f_width = ceil(f.get_width(self.config) / seg_width)
            if f.prev_line:# and f_width <= 4 - line_width:
                if line_width == 0:
                    y_pos += prev_y
                x_pos += (self.config["box_size"] + self.config["box_spacing"]) * self.config[
                    "bool_x_offset"] * line_width
                line_width += f_width
            else:
                y_pos += prev_y
                line_width = f_width

            field_height = f.draw(self.canvas, x_pos + self.config["marker_size"], y_pos, self.config)
            if not f.prev_line or field_height > prev_y:
                prev_y = field_height

            if self.first_sheet:
                data = {
                    "type": f.get_type(),
                    "options": f.get_info(),
                    "id": f.get_id()
                }
                if data["options"] is not None:
                    data["x_pos"] = x_pos
                    data["y_pos"] = y_pos
                    data["height"] = prev_y
                    scan_info.append(data)

        if self.first_sheet:
            json.dump(scan_info, open(filename, "w"))
            self.first_sheet = False

    def _draw_sheets(self):
        for p in range(0, 6):
            for m in range(self.config["init_sheet_num"], self.config["num_sheets"] + 1):
                self._draw_sheet(m, p)
                self.canvas.showPage()
            if self.config["spacer_page"]:
                self.canvas.showPage()
        self.canvas.save()

    def create_from_json(self, sheet_fields):
        self.json_fields = sheet_fields
        field_dict = dict(zip(valid_fields, field_types))
        for field in self.json_fields:
            if field["type"] in field_dict.keys():
                expr = field["type"] + "(**field['options'])"
                f = eval(expr, {"__builtins__": None, 'field': field}, field_dict)
                if "id" in field.keys():
                    f.set_id(field["id"])
                self._add_field(f)
        self.first_sheet = True
        self._draw_sheets()
