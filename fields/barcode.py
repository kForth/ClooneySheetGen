from reportlab.lib.colors import black

import draw_functions as draw
from fields.fieldbase import FieldBase


class Barcode(FieldBase):
    def __init__(self, label, data, digits=4):
        super().__init__()
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
        return self.__class__.__name__

    def get_height(self, config):
        return config["box_size"]

    def _iter(self, img, x_pos, y_pos, config, func, *args, **kwargs):
        x_offset = -config['box_size']
        values = []
        for i in range(self._length):
            values.append(func(
                    img,
                    x_pos + x_offset,
                    y_pos,
                    config["box_size"],
                    *[e(i) if callable(e) else e for e in args],
                    **dict([(k, v(i) if callable(v) else v) for k, v in kwargs.items()])
            ))
            x_offset -= config["box_size"] + config["barcode_spacing"]
        return values

    def draw(self, canvas, x_pos, y_pos, config):
        binary = str(format(int(self.data), '#0' + str(self._length) + 'b'))[2:][::-1]
        width = (config['box_size'] + config['barcode_spacing']) * self._length - config['barcode_spacing']
        draw.rectangle(canvas, x_pos - width, y_pos, width, config['box_size'])
        self._iter(canvas, x_pos, y_pos, config, draw.box,
                    stroke=0, fill_color=black, fill=lambda i: (int(binary[i]) if i < len(binary) else 0))
        return self.get_height(config)
