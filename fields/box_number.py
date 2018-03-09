from fields._base import FieldBase
from fields.string import String
from fields.horizontal_options import HorizontalOptions


class BoxNumber(FieldBase):
    def __init__(self, label, digits=4):
        super().__init__()
        self.label = label
        self.digits = digits

    def get_info(self):
        return {
            "label":  self.label,
            "digits": self.digits
        }

    def get_height(self, config):
        return (config["box_size"] + config["box_spacing"]/2) * self.digits

    def draw_row(self, _img, _x_pos, _y_pos, _config, _i):
        HorizontalOptions("1" + "0" * (self.digits - 1 - _i) + "'s", list(range(0, 10))) \
            .draw(_img, _x_pos, _y_pos + _config["y_spacing"] * (1.5 * _i), _config, False)

    def draw(self, canvas, x_pos, y_pos, config):
        String("Team Number: ____________").draw(canvas, x_pos, y_pos + config["y_spacing"] / 2, config)

        y_pos += config["box_size"] + config["box_spacing"]/2
        for i in range(0, self.digits):
            self.draw_row(canvas, x_pos, y_pos, config, i)

        return self.get_height(config)
