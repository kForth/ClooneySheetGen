import draw_functions as draw
from fields._base import FieldBase


class BulkOptions(FieldBase):
    def __init__(self, label, options, labels, prev_line=False):
        super().__init__()
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
