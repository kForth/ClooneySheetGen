from fields._base import FieldBase

import draw_functions as draw


class Divider(FieldBase):
    def __init__(self, label=None):
        super().__init__()
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
            draw.rectangle(canvas, config["marker_size"], y_pos, self.SHEET_WIDTH - (config["marker_size"] * 2),
                           config["divider_height"])
        else:
            draw.string(canvas, config["marker_size"] + 0.25, y_pos, self.label, config["font_size"] * 1.5)
            draw.rectangle(canvas, config["marker_size"] + 0.125, y_pos + (config["font_size"] * 1.5),
                           self.SHEET_WIDTH - (config["marker_size"] * 2) - 0.25, config["divider_height"],
                           stroke=False, fill=True)
        return self.get_height(config)
