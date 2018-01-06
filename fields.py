import re
from abc import abstractmethod

from reportlab.lib.colors import Color, black

import draw_functions as draw

numbers = [[True, True, True, False, True, True, True],  # 0
           [False, False, True, False, False, True, False],  # 1
           [True, False, True, True, True, False, True],  # 2
           [True, False, True, True, False, True, True],  # 3
           [False, True, True, True, False, True, False],  # 4
           [True, True, False, True, False, True, True],  # 5
           [True, True, False, True, True, True, True],  # 6
           [True, False, True, False, False, True, False],  # 7
           [True, True, True, True, True, True, True],  # 8
           [True, True, True, True, False, True, True],  # 9
           [False, True, False, False, True, False, False],  # Alternate 1
           [False, False, False, False, False, False, False]]  # Blank

positions = [
    "Red 1",
    "Red 2",
    "Red 3",
    "Blue 1",
    "Blue 2",
    "Blue 3"
]

SHEET_WIDTH = 8.5
SHEET_HEIGHT = 11


def get_dump_filename(config):
    return config["filename"] + "_fields.json"


class Field(object):
    def __init__(self):
        self.prev_line = False
        self.id = None

    @abstractmethod
    def _iter(self, *args, **kwargs):
        pass

    def draw(self, *args, **kwargs):
        pass

    def read(self, *args, **kwargs):
        pass

    def set_id(self, data_id):
        self.id = data_id

    def get_id(self):
        return self.id

    def get_height(self, *args):
        return 0

    def get_info(self):
        return None

    def calc_width(self, *args, **kwargs):
        return 0


class Header(Field):
    def __init__(self, match, pos):
        Field.__init__(self)
        self.match = match
        self.pos = pos

    def draw(self, canvas, x_pos, y_pos, config):
        String("Celt-X Team 5406", font_size=0.5).draw(canvas, 0.05 + config["marker_size"],
                                                       0.05 + config["marker_size"], config)
        String("Clooney Scouting System", font_size=3.0 / 32).draw(canvas, 3 + config["marker_size"],
                                                                   0.5 + config["marker_size"], config)
        String(config["event"], font_size=3.0 / 32).draw(canvas, 0.125 + config["marker_size"],
                                                         0.5 + config["marker_size"], config)
        String("Match " + str(self.match) + "    " + positions[self.pos] + "    Scout: _______", font_size=0.25) \
            .draw(canvas, 0.125 + config["marker_size"], 0.625 + config["marker_size"], config)

        match_pos_string = str(self.match)
        while len(match_pos_string) < 3:
            match_pos_string = "0" + match_pos_string
        match_pos_string += str(self.pos)

        barcode = Barcode("-EncodedMatchData", int(match_pos_string))
        barcode.set_id("encoded_match_data")
        barcode_x = 8.5 - config["marker_size"]
        barcode_y = config["marker_size"]
        barcode.draw(canvas, barcode_x, barcode_y, config)

        team_num = BoxNumber("Team Number")
        team_num.set_id("team_number")
        team_num_x = config["x_pos"] + config["marker_size"]
        team_num_y = 1.5
        team_num.draw(canvas, team_num_x, team_num_y, config)

        box_bardcode_info = [
            {
                "type":    barcode.get_type(),
                "id":      barcode.get_id(),
                "options": barcode.get_info(),
                "x_pos":   barcode_x,
                "y_pos":   barcode_y,
                "height":  barcode.get_height(config)
            },
            {
                "type":    team_num.get_type(),
                "id":      team_num.get_id(),
                "options": team_num.get_info(),
                "x_pos":   team_num_x,
                "y_pos":   team_num_y,
                "height":  team_num.get_height(config)

            }
        ]

        return self.get_height(config), box_bardcode_info

    def get_height(self, config):
        return BoxNumber("Team Number").get_height(config)

    def get_type(self):
        return "Header"

    def get_label(self):
        return None


class BoxNumber(Field):
    def __init__(self, label, digits=4):
        Field.__init__(self)
        self.label = label
        self.digits = digits

    def get_info(self):
        return {
            "label":  self.label,
            "digits": self.digits
        }

    def get_label(self):
        return self.label

    def get_type(self):
        return "BoxNumber"

    def get_height(self, config):
        return config["y_spacing"] * (self.digits + 3.5)

    def draw(self, canvas, x_pos, y_pos, config):
        String("Team Number: ____________").draw(canvas, x_pos, y_pos + config["y_spacing"] / 2, config)
        y_pos += config["y_spacing"] * 2
        for i in range(0, self.digits):
            HorizontalOptions("1" + "0" * (self.digits - 1 - i) + "'s", range(0, 10)) \
                .draw(canvas, x_pos, y_pos + config["y_spacing"] * (1.5 * i), config, False)

        return self.get_height(config)


class Barcode(Field):
    def __init__(self, label, data, digits=4):
        Field.__init__(self)
        self.label = label
        self.data = data
        self.digits = digits
        self._length = len(bin(int("9" * self.digits))[2:]) - 3

    def get_info(self):
        return {
            "label":  self.label,
            "digits": self.digits
        }

    def get_label(self):
        return self.label

    def get_type(self):
        return "Barcode"

    def get_height(self, config):
        return config["box_size"]

    def _iter(self, img, x_pos, y_pos, config, func, *args, **kwargs):
        x_offset = -config['box_size']
        for i in range(self._length, 0, -1):
            func(
                    img,
                    x_pos + x_offset,
                    y_pos,
                    config["box_size"],
                    *[e(i) if callable(e) else e for e in args],
                    **dict([(k, v(i) if callable(v) else v) for k, v in kwargs.items()])
                 )
            x_offset -= config["box_size"] + config["barcode_spacing"]

    def draw(self, canvas, x_pos, y_pos, config):
        binary = str(format(int(self.data), '#0' + str(self._length) + 'b'))[2:]
        width = (config['box_size'] + config['barcode_spacing']) * self._length
        draw.rectangle(canvas, x_pos - width, y_pos, width, config['box_size'])
        self._iter(canvas, x_pos, y_pos, config, draw.box, stroke=0, fill_color=black,
                   fill=lambda i: (int(binary[i]) if i < len(binary) else 0))

        return self.get_height(config)


class HorizontalOptions(Field):
    def __init__(self, label, options: list, prev_line=False, offset=0, note_space=False, note_width=3):
        Field.__init__(self)
        self.label = label
        self.options = options
        self.prev_line = prev_line
        self.offset = offset
        self.note_space = note_space
        self.note_width = note_width

    def get_info(self):
        return {
            "label":      self.label,
            "options":    self.options,
            "offset":     self.offset,
            "note_space": self.note_space,
            "note_width": self.note_width,
            "type":       self.get_type()
        }

    def get_label(self):
        return self.label

    def get_height(self, config):
        return config["font_size"] + config["y_spacing"]

    def _iter(self, img, x_pos, y_pos, config, func, *args, **kwargs):
        pass

    def draw(self, canvas, x_pos, y_pos, config, dump_info=True):
        x_offset = self.offset
        draw.string(canvas, x_pos + x_offset, y_pos + ((config["box_size"] - config["font_size"]) / 2.0),
                    self.label + (":" if not self.label == "" else ""), config["font_size"])

        if self.note_space:
            x = x_pos + config["label_offset"]
            draw.rectangle(canvas, x, y_pos,
                           self.note_width * (config["box_size"] + config["box_spacing"]) + config["box_size"],
                           config["box_size"])
            x_pos += (1 + self.note_width) * (config["box_size"] + config["box_spacing"])

        x_offset += config["label_offset"]
        font_size = config["box_font_size"]
        for op in self.options:
            if type(op) == list:
                o = op[0]
            else:
                o = op
            if o == '.':
                x_offset += config["box_spacing"] + config["box_size"]
                continue
            if o == ',':
                x_offset += config["box_spacing"]
                continue
            if o == "_":
                o = " "
            draw.box(canvas, x_pos + x_offset, y_pos, config["box_size"], label=str(o), font_size=font_size)
            x_offset += config["box_spacing"] + config["box_size"]

        return self.get_height(config)

    def calc_width(self, config):
        width = config["label_offset"] + int(self.note_space) * (self.note_width + config["box_spacing"]) + \
                (config["box_size"] + config["box_spacing"]) * len(self.options)

        return width

    def get_type(self):
        return "HorizontalOptions"


class BulkOptions(Field):
    def __init__(self, label, options, labels, prev_line=False):
        Field.__init__(self)
        self.label = label
        self.options = options
        self.labels = labels
        self.prev_line = prev_line

    def get_info(self):
        return {
            "label":   self.label,
            "options": self.options,
            "labels":  self.labels
        }

    def get_label(self):
        return self.label

    def get_height(self, config):
        if self.prev_line:
            return config["y_spacing"] + config["box_spacing"]
        else:
            return config["font_size"] * 2 + (config["y_spacing"] + config["box_spacing"]) * len(self.options)

    def draw(self, canvas, x_pos, y_pos, config):
        if self.prev_line:
            y_pos -= 2.74 * (config["font_size"] + config["y_spacing"])
            x_pos += 4
        draw.string(canvas, x_pos, y_pos + ((config["box_size"] - config["font_size"]) / 2.0), self.label + ":",
                    config["font_size"])
        x_offset = 1
        for i in range(len(self.labels)):
            draw.string(canvas, x_pos + x_offset + (config["box_spacing"] + config["box_size"]) * i,
                        y_pos + ((config["box_size"] - config["font_size"]) / 2.0), self.labels[i], config["font_size"])
        y_pos += config["font_size"] + config["box_spacing"]
        for i in range(len(self.labels)):
            label = self.labels[i]
            for j in range(len(self.options)):
                o = self.options[j]
                if o == '.':
                    x_offset += config["box_spacing"] + config["box_size"]
                    continue
                if o == ',':
                    x_offset += config["box_spacing"]
                    continue
                draw.box(canvas, x_pos + x_offset, y_pos + j * (config["y_spacing"] + config["box_spacing"]),
                         config["box_size"], label=o, font_size=config["box_font_size"])
            x_offset += config["box_spacing"] + config["box_size"]

        return self.get_height(config)

    def get_type(self):
        return "BulkOptions"


class Numbers(HorizontalOptions):
    def __init__(self, label, ones=9, tens=0, show_zero=False, **kwargs):
        options = []
        for i in range(0 if show_zero else 1, ones + 1):
            options.append(str(i))
        if tens > 0:
            for j in range(1, tens + 1):
                options.append("+10")

        HorizontalOptions.__init__(self, label, options, **kwargs)

    def get_info(self):
        d = HorizontalOptions.get_info(self)
        d = HorizontalOptions.get_info(self)
        d["type"] = self.get_type()
        return d

    def draw(self, canvas, x_pos, y_pos, config, *args):
        return HorizontalOptions.draw(self, canvas, x_pos, y_pos, config)

    def get_type(self):
        return "Numbers"


class Image(Field):
    def __init__(self, label, width, height, image_path, prev_line=False, offset=4.25, y_offset=1):
        Field.__init__(self)
        self.label = label
        self.width = width
        self.height = height
        self.image_path = image_path
        self.prev_line = prev_line
        self.offset = offset
        self.y_offset = y_offset

    def get_info(self):
        return {
            "label":     self.label,
            "width":     self.width,
            "height":    self.height,
            "offset":    self.width,
            "y_offset":  self.width,
            "prev_line": self.prev_line
        }

    def get_label(self):
        return self.label

    def get_type(self):
        return "Image"

    def get_height(self, config):
        if self.prev_line:
            return 0
        else:
            return self.height + config["y_spacing"]

    def draw(self, canvas, x_pos, y_pos, config):
        if self.prev_line:
            x_pos += self.offset
            y_pos -= self.y_offset + 0.2375
            draw.string(canvas, x_pos + 1,
                        y_pos + ((config["box_size"] - config["font_size"]) / 2.0) - config["y_spacing"],
                        self.label + ":", config["font_size"])
        else:
            draw.string(canvas, x_pos, y_pos + ((config["box_size"] - config["font_size"]) / 2.0), self.label + ":",
                        config["font_size"])
        draw.rectangle(canvas, x_pos + 1, y_pos, self.width, self.height)
        if self.image_path is not None:
            draw.image(canvas, x_pos + 1, y_pos, self.width, self.height, self.image_path)

        return self.get_height(config)


class Boolean(HorizontalOptions):
    def __init__(self, label, prev_line=False, offset=0):
        HorizontalOptions.__init__(self, label, ["_"], prev_line, offset)

    def get_info(self):
        d = HorizontalOptions.get_info(self)
        d["type"] = self.get_type()
        return d

    def draw(self, canvas, x_pos, y_pos, config, *args):
        return HorizontalOptions.draw(self, canvas, x_pos, y_pos, config)

    def get_type(self):
        return "Boolean"


class Divider(Field):
    def __init__(self, label=None):
        Field.__init__(self)
        self.label = label

    def get_height(self, config):
        if self.label is None:
            return config["y_spacing"]
        elif self.label == "-":
            return 0
        else:
            return config["font_size"] * 1.5 + config["divider_height"] + config["y_spacing"]

    def draw(self, canvas, x_pos, y_pos, config):
        if self.label is None:
            pass
        elif self.label == "-":
            draw.rectangle(canvas, config["marker_size"], y_pos, SHEET_WIDTH - (config["marker_size"] * 2),
                           config["divider_height"])
        else:
            draw.string(canvas, config["marker_size"] + 0.25, y_pos, self.label, config["font_size"] * 1.5)
            draw.rectangle(canvas, config["marker_size"] + 0.125, y_pos + (config["font_size"] * 1.5),
                           SHEET_WIDTH - (config["marker_size"] * 2) - 0.25, config["divider_height"], stroke=False,
                           fill=True)
        return self.get_height(config)

    def get_type(self):
        return "Divider"

    def get_label(self):
        return self.label


class Markers(Field):
    def draw(self, canvas, config):
        Field.__init__(self)
        marker_color = Color(*config["marker_colour"], alpha=1.0)
        draw.box(canvas,
                 0,
                 0,
                 config["marker_size"], stroke=0, fill=1, fill_color=marker_color)
        draw.box(canvas,
                 SHEET_WIDTH - config["marker_size"],
                 0,
                 config["marker_size"], stroke=0, fill=1, fill_color=marker_color)
        draw.box(canvas,
                 0,
                 SHEET_HEIGHT - config["marker_size"],
                 config["marker_size"], stroke=0, fill=1, fill_color=marker_color)
        draw.box(canvas,
                 SHEET_WIDTH - config["marker_size"],
                 SHEET_HEIGHT - config["marker_size"],
                 config["marker_size"], stroke=0, fill=1, fill_color=marker_color)
        draw.rectangle(canvas, config["marker_size"], config["marker_size"],
                       SHEET_WIDTH - config["marker_size"] * 2,
                       SHEET_HEIGHT - config["marker_size"] * 2)

    def get_type(self):
        return "Markers"

    def get_label(self):
        return None


class SevenSegment(Field):
    def __init__(self, value=11):
        Field.__init__(self)
        if value == " ":
            value = 11
        self.value = value

    def draw(self, canvas, x_pos, y_pos, config):
        width = config["seven_segment_width"]
        thickness = config["seven_segment_thickness"]
        draw.rectangle(canvas, x_pos + thickness, y_pos, width, thickness, fill=numbers[self.value][0])
        draw.rectangle(canvas, x_pos, y_pos + thickness, thickness, width, fill=numbers[self.value][1])
        draw.rectangle(canvas, x_pos + thickness + width, y_pos + thickness, thickness, width,
                       fill=numbers[self.value][2])
        draw.rectangle(canvas, x_pos + thickness, y_pos + thickness + width, width, thickness,
                       fill=numbers[self.value][3])
        draw.rectangle(canvas, x_pos, y_pos + thickness * 2 + width, thickness, width, fill=numbers[self.value][4])
        draw.rectangle(canvas, x_pos + thickness + width, y_pos + thickness * 2 + width, thickness, width,
                       fill=numbers[self.value][5])
        draw.rectangle(canvas, x_pos + thickness, y_pos + width * 2 + thickness * 2, width, thickness,
                       fill=numbers[self.value][6])
        return self.get_height(config)

    def get_height(self, config):
        return config["seven_segment_width"] * 2 + config["seven_segment_thickness"] * 3 + config["y_spacing"]

    def get_type(self):
        return "SevenSegment"

    def get_label(self):
        return None


class Digits(Field):
    def __init__(self, label, digits=4, values="11 11 11 11"):
        Field.__init__(self)
        self.digits = digits
        self.label = label
        self.values = values

    def get_info(self):
        return {
            "label":  self.label,
            "digits": self.digits
        }

    def draw(self, canvas, x_pos, y_pos, config):
        if not self.label[0] == "-":
            draw.string(canvas, x_pos, y_pos, self.label + ":", config["font_size"])
            for i in range(self.digits):
                SevenSegment(value=int(self.values.split(" ")[i])).draw(canvas,
                                                                        x_pos + 1 + config["seven_segment_offset"] * i,
                                                                        y_pos, config)
        elif self.label == "-TeamNumber":
            for i in range(self.digits):
                SevenSegment(value=int(self.values.split(" ")[i])).draw(canvas,
                                                                        x_pos + config["seven_segment_offset"] * i,
                                                                        y_pos, config)
            draw.string(canvas, x_pos,
                        y_pos + config["seven_segment_width"] * 2 + config["seven_segment_thickness"] * 3 + config[
                            "y_spacing"], "Team #: __________", config["font_size"])
        else:
            for i in range(self.digits):
                SevenSegment(value=int(self.values.split(" ")[i])).draw(canvas,
                                                                        x_pos + config["seven_segment_offset"] * i,
                                                                        y_pos, config)
            draw.string(canvas, x_pos,
                        y_pos + config["seven_segment_width"] * 2 + config["seven_segment_thickness"] * 3 + config[
                            "box_spacing"], re.sub(r"(?<=\w)([A-Z])", r" \1", self.label[1:]), config["font_size"])

        return self.get_height(config)

    def get_type(self):
        return "Digits"

    def get_height(self, config):
        return 0.6875 + config["y_spacing"]

    def get_label(self):
        return self.label


class String(Field):
    def __init__(self, string, font_size=-1, pos=(0, 0), height="normal", x_offset=0):
        Field.__init__(self)
        self.string = string
        self.font_size = font_size
        self.pos = pos
        self.height = height
        self.x_offset = x_offset

    def draw(self, canvas, x_pos, y_pos, config):
        if not self.pos == (0, 0):
            x_pos = self.pos[0]
            y_pos = self.pos[1]
        else:
            x_pos += self.x_offset
        if self.height == "thin":
            y_pos -= config["y_spacing"] / 8
        font_size = self.font_size
        if font_size == -1:
            font_size = config["font_size"]
        draw.string(canvas, x_pos, y_pos, self.string, font_size)
        return self.get_height(config)

    def get_height(self, config):
        if not self.pos == (0, 0):
            return 0
        else:
            if self.height == "thin":
                return self.font_size + config["y_spacing"] / 8
            else:
                return self.font_size + config["y_spacing"]

    def get_type(self):
        return "String"

    def get_label(self):
        return None
