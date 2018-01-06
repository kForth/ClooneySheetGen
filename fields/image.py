import draw_functions as draw
from fields._base import FieldBase


class Image(FieldBase):
    def __init__(self, label, width, height, image_path, prev_line=False, offset=4.25, y_offset=1):
        super().__init__()
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

    def get_width(self, _):
        return self.width

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
