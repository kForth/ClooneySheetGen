from fields.horizontal_options import HorizontalOptions


class Boolean(HorizontalOptions):
    def __init__(self, label, prev_line=False, offset=0):
        HorizontalOptions.__init__(self, label, ["_"], prev_line, offset)

    def get_info(self):
        d = HorizontalOptions.get_info(self)
        d["type"] = self.get_type()
        return d

    def draw(self, canvas, x_pos, y_pos, config, *args):
        return HorizontalOptions.draw(self, canvas, x_pos, y_pos, config)

    def get_type(self):
        return self.__class__.__name__
