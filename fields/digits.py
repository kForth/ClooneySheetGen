import draw_functions as draw
from fields.seven_segment import SevenSegment
from fields.fieldbase import FieldBase


class Digits(FieldBase):
    def __init__(self, label, digits=4, values="11 11 11 11"):
        super().__init__()
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
        return self.__class__.__name__

    def get_height(self, config):
        return 0.6875 + config["y_spacing"]

    def get_label(self):
        return self.label
