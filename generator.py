import json

import Fields
from Sheet import *

config = {
    "num_sheets":              1,
    "filename":                "Steamworks2",
    "encode_scanner":          True,
    "event":                   "Test 2017",
    "spacer_page":             True,
    "x_pos":                   0.25,
    "y_spacing":               0.18,
    "box_size":                0.18,  # 0.2
    "box_spacing":             0.1,
    "bool_x_offset":           6,
    "font_size":               0.12,  # 0.15
    "box_font_size":           0.1,
    "marker_size":             0.5,
    "divider_height":          1.0 / 64,
    "team_x_offset":           5.6875,
    "seven_segment_width":     0.25,
    "seven_segment_thickness": 0.0625,
    "seven_segment_offset":    0.5,
    "marker_colour":           (255, 0, 0),
    "font_color":              (100, 100, 100),
    "label_offset":            1.25
    }

field_types = [Fields.Barcode, Fields.Boolean, Fields.BoxNumber, Fields.BulkOptions, Fields.Digits,
               Fields.Divider, Fields.Header, Fields.HorizontalOptions, Fields.Image, Fields.Markers,
               Fields.Numbers, Fields.SevenSegment, Fields.String]
valid_fields = map(lambda x: x.__name__, field_types)


class Generator(object):
    def __init__(self, config):
        self.config = config

    def create(self, sheet_fields):
        sheet = Sheet(self.config)
        field_dict = dict(zip(valid_fields, field_types))
        for field in sheet_fields:
            if field["type"] in field_dict.keys():
                expr = field["type"] + "(**field['options'])"
                sheet.add_field(eval(expr, {"__builtins__": None, 'field': field}, field_dict))
        sheet.draw_sheets()


if __name__ == "__main__":
    gen = Generator(config)
    fields = json.load(open("steamworks.json", "r"))
    gen.create(fields)
