from fields.fieldbase import FieldBase
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

    def get_label(self):
        return self.label

    def get_type(self):
        return self.__class__.__name__

    def get_height(self, config):
        return config["y_spacing"] * (self.digits + 3.5)

    def draw(self, canvas, x_pos, y_pos, config):
        String("Team Number: ____________").draw(canvas, x_pos, y_pos + config["y_spacing"] / 2, config)
        y_pos += config["y_spacing"] * 2
        for i in range(0, self.digits):
            HorizontalOptions("1" + "0" * (self.digits - 1 - i) + "'s", list(range(0, 10))) \
                .draw(canvas, x_pos, y_pos + config["y_spacing"] * (1.5 * i), config, False)

        return self.get_height(config)
