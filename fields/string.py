from reportlab.pdfbase.pdfmetrics import stringWidth

from fields._base import FieldBase
import draw_functions as draw


class String(FieldBase):
    def __init__(self, string, font_size=-1.0, pos=(0, 0), height="normal", x_offset=0):
        super().__init__()
        self.string = string
        self.font_size = font_size
        self.pos = pos
        self.height = height
        self.x_offset = x_offset

    def _iter(self, img, x_pos, y_pos, config, func, *args, **kwargs):
        pass

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
        print(self.get_width(config))
        return self.get_height(config)

    def get_width(self, config):
        return stringWidth(self.string, 'OpenSansEmoji', self.font_size)

    def get_height(self, config):
        if not self.pos == (0, 0):
            return 0
        else:
            if self.height == "thin":
                return self.font_size + config["y_spacing"] / 8
            else:
                return self.font_size + config["y_spacing"]
