from fields.horizontal_options import HorizontalOptions


class Boolean(HorizontalOptions):
    def __init__(self, label, prev_line=False, offset=0):
        HorizontalOptions.__init__(self, label, ["_"], prev_line, offset)
