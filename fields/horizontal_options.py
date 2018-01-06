import draw_functions as draw
from fields._base import FieldBase


class HorizontalOptions(FieldBase):
    def __init__(self, label, options: list, prev_line=False, offset=0, note_space=False, note_width=3):
        super().__init__()
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

    def get_height(self, config):
        return config["font_size"] + config["y_spacing"]

    def get_width(self, config):
        return config["label_offset"] + int(self.note_space) * (self.note_width + config["box_spacing"]) + \
               (config["box_size"] + config["box_spacing"]) * len(self.options)

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
