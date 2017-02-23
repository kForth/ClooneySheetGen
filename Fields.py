import re

from reportlab.lib import colors

from DrawFunctions import *

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

positions = ["Red 1",
             "Red 2",
             "Red 3",
             "Blue 1",
             "Blue 2",
             "Blue 3"]

SHEET_WIDTH = 8.5  # 8.375
SHEET_HEIGHT = 11  # 10.875


class Field(object):
    def __init__(self):
        self.prev_line = False

    def calc_width(self, *args, **kwargs):
        return 0


class Header(Field):
    def __init__(self, match, pos):
        Field.__init__(self)
        self.match = match
        self.pos = pos

    def draw(self, canvas, x_pos, y_pos, config):
        x_pos = 0
        y_pos = 0
        String("Celt-X Team 5406", font_size=0.5).draw(canvas, 0.05 + config["marker_size"],
                                                       0.05 + config["marker_size"], config)
        String("Clooney Scouting System", font_size=3.0 / 32).draw(canvas, 3 + config["marker_size"],
                                                                   0.5 + config["marker_size"], config)
        String(config["event"], font_size=3.0 / 32).draw(canvas, 0.125 + config["marker_size"],
                                                         0.5 + config["marker_size"], config)
        String("Match " + str(self.match) + "    " + positions[self.pos] + "    Scout: _______", font_size=0.25).draw(
            canvas, 0.125 + config["marker_size"], 0.625 + config["marker_size"], config)

        match_pos_string = str(self.match)
        while len(match_pos_string) < 3:
            match_pos_string = "0" + match_pos_string
        match_pos_string += str(self.pos)

        Barcode("-EncodedMatchData", int(match_pos_string)).draw(canvas, 8.5 - config["marker_size"] - 0.325,
                                                                 config["marker_size"], config)

        y_pos += 1.5
        x_pos += config["x_pos"] + config["marker_size"]
        return BoxNumber("Team Number").draw(canvas, x_pos, y_pos, config)

    def get_type(self):
        return "Header"

    def get_label(self):
        return None


class BoxNumber(Field):
    def __init__(self, label, digits=4, prev_line=False, offset=0):
        Field.__init__(self)
        self.label = label
        self.digits = digits
        self.prev_line = prev_line
        self.offset = offset

    def get_label(self):
        return self.label

    def get_type(self):
        return "BoxNumber"

    def draw(self, canvas, x_pos, y_pos, config):
        String("Team Number: ____________").draw(canvas, x_pos, y_pos + config["y_spacing"] / 2, config)
        y_pos += config["y_spacing"] * 2
        for i in range(0, self.digits):
            HorizontalOptions("1" + "0" * (self.digits - 1 - i) + "'s", range(0, 10)).draw(canvas, x_pos,
                                                                                           y_pos + config[
                                                                                               "y_spacing"] * (1.5 * i),
                                                                                           config, False)

        with open("StrongholdFields.csv", "a") as f:
            if self.label == "":
                self.label = "-"
            f.write(self.get_type() + "," + self.label + "," + str(self.digits) + "," + str(x_pos + 1) + "," + str(
                y_pos) + "," + str(config["box_size"]) + "," + str(config["box_spacing"]) + "," + str(
                    config["y_spacing"]) + "\n")

        return config["y_spacing"] * (self.digits + 3.5)


class Barcode(Field):
    def __init__(self, label, data, digits=4):
        Field.__init__(self)
        self.label = label
        self.data = data
        self.digits = digits

    def get_label(self):
        return self.label

    def get_type(self):
        return "Barcode"

    def draw(self, canvas, x_pos, y_pos, config):
        length = len(bin(int("9" * self.digits))[2:])
        binary = str(format(int(self.data), '#0' + str(length) + 'b'))[2:]
        x_offset = 0
        for i in range(len(binary), 0, -1):
            draw_square(canvas, x_pos + x_offset, y_pos, config["box_size"], outline=1, infill=int(binary[i - 1]))
            x_offset -= config["box_size"]

        with open("StrongholdFields.csv", "a") as f:
            f.write(self.get_type() + "," + self.label + "," + str(self.digits) + "," + str(x_pos) + "," + str(
                y_pos) + "," + str(config["box_size"]) + "\n")

        return 0


class HorizontalOptions(Field):
    def __init__(self, label, options, prev_line=False, offset=0, note_space=False, note_width=3):
        Field.__init__(self)
        self.label = label
        self.options = options
        self.prev_line = prev_line
        self.offset = offset
        self.note_space = note_space
        self.note_width = note_width

    def get_label(self):
        return self.label

    def draw(self, canvas, x_pos, y_pos, config, dump_info=True):
        x_offset = self.offset
        draw_string(canvas, x_pos + x_offset, y_pos + ((config["box_size"] - config["font_size"]) / 2.0),
                    self.label + (":" if not self.label == "" else ""), config["font_size"])

        if self.note_space:
            x = x_pos + config["label_offset"]
            draw_rect(canvas, x, y_pos,
                      self.note_width * (config["box_size"] + config["box_spacing"]) + config["box_size"],
                      config["box_size"])
            x_pos += (1 + self.note_width) * (config["box_size"] + config["box_spacing"])

        x_offset += config["label_offset"]
        font_size = config["box_font_size"]
        for o in self.options:
            if o == '.':
                x_offset += config["box_spacing"] + config["box_size"]
                continue
            if o == ',':
                x_offset += config["box_spacing"]
                continue
            if o == "_":
                o = " "
            draw_square(canvas, x_pos + x_offset, y_pos, config["box_size"], label=str(o), font_size=font_size)
            x_offset += config["box_spacing"] + config["box_size"]

        if dump_info:
            with open("StrongholdFields.csv", "a") as f:
                if self.label == "":
                    self.label = self.label_backup
                f.write(self.get_type() + "," + self.label + "," + str(x_pos + 1 + self.offset) + "," + str(
                    y_pos) + "," + str(config["box_size"]) + "," + str(config["box_spacing"]) + "," + " ".join(
                    self.options) + "\n")

        return config["font_size"] + config["y_spacing"]

    def calc_width(self, config):
        width = config["label_offset"] + int(self.note_space) * (self.note_width + config["box_spacing"]) + (config[
                                                                                                                 "box_size"] +
                                                                                                             config[
                                                                                                                 "box_spacing"]) * len(
            self.options)
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

    def get_label(self):
        return self.label

    def draw(self, canvas, x_pos, y_pos, config):
        if self.prev_line:
            y_pos -= 2.74 * (config["font_size"] + config["y_spacing"])
            x_pos += 4
        draw_string(canvas, x_pos, y_pos + ((config["box_size"] - config["font_size"]) / 2.0), self.label + ":",
                    config["font_size"])
        x_offset = 1
        for i in range(len(self.labels)):
            draw_string(canvas, x_pos + x_offset + (config["box_spacing"] + config["box_size"]) * i,
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
                draw_square(canvas, x_pos + x_offset, y_pos + j * (config["y_spacing"] + config["box_spacing"]),
                            config["box_size"], label=o, font_size=config["box_font_size"])
            x_offset += config["box_spacing"] + config["box_size"]

        with open("StrongholdFields.csv", "a") as f:
            f.write(self.get_type() + "," + self.label + "," + " ".join(self.labels) + "," + str(x_pos + 1) + "," + str(
                y_pos) + "," + str(config["box_size"]) + "," + str(config["box_spacing"]) + "," + self.options + "\n")

        if self.prev_line:
            return (config["y_spacing"] + config["box_spacing"])
        else:
            return config["font_size"] * 2 + (config["y_spacing"] + config["box_spacing"]) * len(self.options)

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

    def draw(self, canvas, x_pos, y_pos, config):
        offset = HorizontalOptions.draw(self, canvas, x_pos, y_pos, config)
        return offset

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

    def get_label(self):
        return self.label

    def get_type(self):
        return "Image"

    def draw(self, canvas, x_pos, y_pos, config):
        if self.prev_line:
            x_pos += self.offset
            y_pos -= self.y_offset + 0.2375
            draw_string(canvas, x_pos + 1,
                        y_pos + ((config["box_size"] - config["font_size"]) / 2.0) - config["y_spacing"],
                        self.label + ":", config["font_size"])
        else:
            draw_string(canvas, x_pos, y_pos + ((config["box_size"] - config["font_size"]) / 2.0), self.label + ":",
                        config["font_size"])
        draw_rect(canvas, x_pos + 1, y_pos, self.width, self.height)
        if self.image_path != None:
            draw_image(canvas, x_pos + 1, y_pos, self.width, self.height, self.image_path)

        with open("StrongholdFields.csv", "a") as f:
            f.write(self.get_type() + "," + self.label + "," + str(x_pos + 1) + "," + str(y_pos) + "," + str(
                self.width) + "," + str(self.height) + "\n")

        if self.prev_line:
            return 0
        else:
            return self.height + config["y_spacing"]


class Boolean(HorizontalOptions):
    def __init__(self, label, prev_line=False, offset=0):
        HorizontalOptions.__init__(self, label, "_", prev_line, offset)

    def draw(self, canvas, x_pos, y_pos, config):
        HorizontalOptions.draw(self, canvas, x_pos, y_pos, config)
        return config["font_size"] + config["y_spacing"]

    def get_type(self):
        return "Boolean"


class Divider(Field):
    def __init__(self, label=None):
        Field.__init__(self)
        self.label = label

    def draw(self, canvas, x_pos, y_pos, config):
        if self.label == None:
            return config["y_spacing"]
        if self.label == "-":
            draw_rect(canvas, config["marker_size"], y_pos, SHEET_WIDTH - (config["marker_size"] * 2),
                      config["divider_height"])
            return
        else:
            draw_string(canvas, config["marker_size"] + 0.25, y_pos, self.label, config["font_size"] * 1.5)
            draw_rect(canvas, config["marker_size"] + 0.125, y_pos + (config["font_size"] * 1.5),
                      SHEET_WIDTH - (config["marker_size"] * 2) - 0.25, config["divider_height"], outline=False, infill=True)
            return config["font_size"] * 1.5 + config["divider_height"] + config["y_spacing"]

    def get_type(self):
        return "Divider"

    def get_label(self):
        return self.label


class Markers(Field):
    def draw(self, canvas, config):
        Field.__init__(self)
        canvas.setFillColor(config["marker_colour"])
        draw_square(canvas, 0, 0, config["marker_size"], outline=False, infill=True)
        draw_square(canvas, SHEET_WIDTH - config["marker_size"], SHEET_HEIGHT - config["marker_size"], config["marker_size"],
                    outline=False, infill=True)
        canvas.setFillColor(colors.black)
        draw_rect(canvas, config["marker_size"], config["marker_size"], SHEET_WIDTH - config["marker_size"] * 2,
                  SHEET_HEIGHT - config["marker_size"] * 2)

        with open("StrongholdFields.csv", "a") as f:
            f.write(self.get_type() + "," + str(config["marker_size"]) + "," + ",".join(
                map(str, config["marker_colour"])) + "\n")

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
        draw_rect(canvas, x_pos + thickness, y_pos, width, thickness, infill=numbers[self.value][0])
        draw_rect(canvas, x_pos, y_pos + thickness, thickness, width, infill=numbers[self.value][1])
        draw_rect(canvas, x_pos + thickness + width, y_pos + thickness, thickness, width, infill=numbers[self.value][2])
        draw_rect(canvas, x_pos + thickness, y_pos + thickness + width, width, thickness, infill=numbers[self.value][3])
        draw_rect(canvas, x_pos, y_pos + thickness * 2 + width, thickness, width, infill=numbers[self.value][4])
        draw_rect(canvas, x_pos + thickness + width, y_pos + thickness * 2 + width, thickness, width,
                  infill=numbers[self.value][5])
        draw_rect(canvas, x_pos + thickness, y_pos + width * 2 + thickness * 2, width, thickness,
                  infill=numbers[self.value][6])
        return width * 2 + thickness * 3 + config["y_spacing"]

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

    def get_type(self):
        return "Digits"

    def draw(self, canvas, x_pos, y_pos, config):
        if not self.label[0] == "-":
            draw_string(canvas, x_pos, y_pos, self.label + ":", config["font_size"])
            for i in range(self.digits):
                SevenSegment(value=int(self.values.split(" ")[i])).draw(canvas,
                                                                        x_pos + 1 + config["seven_segment_offset"] * i,
                                                                        y_pos, config)
        elif self.label == "-TeamNumber":
            for i in range(self.digits):
                SevenSegment(value=int(self.values.split(" ")[i])).draw(canvas,
                                                                        x_pos + config["seven_segment_offset"] * i,
                                                                        y_pos, config)
            draw_string(canvas, x_pos,
                        y_pos + config["seven_segment_width"] * 2 + config["seven_segment_thickness"] * 3 + config[
                            "y_spacing"], "Team #: __________", config["font_size"])
        else:
            for i in range(self.digits):
                SevenSegment(value=int(self.values.split(" ")[i])).draw(canvas,
                                                                        x_pos + config["seven_segment_offset"] * i,
                                                                        y_pos, config)
            draw_string(canvas, x_pos,
                        y_pos + config["seven_segment_width"] * 2 + config["seven_segment_thickness"] * 3 + config[
                            "box_spacing"], re.sub(r"(?<=\w)([A-Z])", r" \1", self.label[1:]), config["font_size"])

        with open("StrongholdFields.csv", "a") as f:
            f.write(self.get_type() + "," + self.label + "," + str(x_pos) + "," + str(y_pos) + "," + str(
                    config["seven_segment_width"]) + "," + str(config["seven_segment_thickness"]) + "," + str(
                    config["seven_segment_offset"]) + "\n")

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
        draw_string(canvas, x_pos, y_pos, self.string, font_size)
        if not self.pos == (0, 0):
            return 0
        else:
            if self.height == "thin":
                return font_size + config["y_spacing"] / 8
            else:
                return font_size + config["y_spacing"]

    def get_type(self):
        return "String"

    def get_label(self):
        return None
